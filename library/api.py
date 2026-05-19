import json
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .models import Book, Profile


def _json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return None


def _user_payload(user: User):
    profile = getattr(user, "library_profile", None)
    role = profile.role if profile else Profile.ROLE_USER
    return {
        "fullName": user.first_name or user.username,
        "email": user.email or user.username,
        "role": role,
    }


def _book_public(book: Book):
    return {
        "id": book.slug,
        "slug": book.slug,
        "title": book.title,
        "author": book.author,
        "status": book.status,
        "category": book.tags or [],
        "description": book.description,
        "shelfCategory": book.shelf_category,
    }


def _book_admin_row(book: Book):
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "category": book.shelf_category or (book.tags[0] if book.tags else ""),
        "available": book.status == Book.STATUS_AVAILABLE,
        "status": book.status,
    }


def _require_user(request):
    if not request.user.is_authenticated:
        return None, JsonResponse({"error": "Authentication required"}, status=401)
    return request.user, None


def _require_admin(request):
    user, err = _require_user(request)
    if err:
        return None, err
    profile = getattr(user, "library_profile", None)
    if not profile or profile.role != Profile.ROLE_ADMIN:
        return None, JsonResponse({"error": "Admin access only"}, status=403)
    return user, None


def _is_admin_user(user: User) -> bool:
    profile = getattr(user, "library_profile", None)
    return bool(profile and profile.role == Profile.ROLE_ADMIN)


@csrf_exempt
@require_http_methods(["POST"])
def api_register(request):
    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    full_name = (data.get("fullName") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role = data.get("role") or Profile.ROLE_USER

    if role not in (Profile.ROLE_ADMIN, Profile.ROLE_USER):
        role = Profile.ROLE_USER

    if not full_name or not email or not password:
        return JsonResponse({"error": "Please fill in all fields."}, status=400)

    if User.objects.filter(username=email).exists():
        return JsonResponse({"error": "Email already exists."}, status=400)

    if len(password) < 6:
        return JsonResponse({"error": "Password must be at least 6 characters."}, status=400)

    with transaction.atomic():
        user = User.objects.create_user(username=email, email=email, password=password, first_name=full_name)
        Profile.objects.create(user=user, role=role)

    return JsonResponse({"ok": True, "user": _user_payload(user)})


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return JsonResponse({"error": "Please fill in all fields."}, status=400)

    user = authenticate(request, username=email, password=password)
    if user is None:
        return JsonResponse({"error": "Incorrect email or password."}, status=401)

    login(request, user)
    return JsonResponse({"ok": True, "user": _user_payload(user)})


@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request):
    logout(request)
    return JsonResponse({"ok": True})


@csrf_exempt
@require_GET
def api_me(request):
    user, err = _require_user(request)
    if err:
        return err
    return JsonResponse({"user": _user_payload(user)})


@csrf_exempt
@require_GET
def api_books_list(request):
    _, err = _require_user(request)
    if err:
        return err
    books = Book.objects.all()
    return JsonResponse({"books": [_book_public(b) for b in books]})


@csrf_exempt
@require_GET
def api_book_detail(request, slug):
    _, err = _require_user(request)
    if err:
        return err
    book = Book.objects.filter(slug=slug).first()
    if not book:
        return JsonResponse({"error": "Not found"}, status=404)
    return JsonResponse({"book": _book_public(book)})


@csrf_exempt
@require_http_methods(["POST"])
def api_book_borrow(request, slug):
    user, err = _require_user(request)
    if err:
        return err

    book = Book.objects.filter(slug=slug).first()
    if not book:
        return JsonResponse({"error": "Not found"}, status=404)
    if book.status != Book.STATUS_AVAILABLE:
        return JsonResponse({"error": "Book is not available"}, status=400)

    today = timezone.localdate()
    book.status = Book.STATUS_BORROWED
    book.borrowed_by = user
    book.borrow_date = today
    book.return_deadline = today + timedelta(days=14)
    book.save()
    return JsonResponse({"ok": True, "book": _book_public(book)})


@csrf_exempt
@require_http_methods(["POST"])
def api_book_return(request, slug):
    user, err = _require_user(request)
    if err:
        return err

    is_admin = _is_admin_user(user)

    book = Book.objects.filter(slug=slug).first()
    if not book:
        return JsonResponse({"error": "Not found"}, status=404)
    if book.status != Book.STATUS_BORROWED:
        return JsonResponse({"error": "Book is not borrowed"}, status=400)
    if not is_admin and book.borrowed_by_id != user.id:
        return JsonResponse({"error": "You cannot return this book"}, status=403)

    book.status = Book.STATUS_AVAILABLE
    book.borrowed_by = None
    book.borrow_date = None
    book.return_deadline = None
    book.save()
    return JsonResponse({"ok": True, "book": _book_public(book)})


@csrf_exempt
@require_GET
def api_borrowed_list(request):
    user, err = _require_user(request)
    if err:
        return err

    books = Book.objects.filter(borrowed_by=user, status=Book.STATUS_BORROWED)
    payload = []
    for b in books:
        payload.append(
            {
                "id": b.slug,
                "title": b.title,
                "author": b.author,
                "borrowDate": b.borrow_date.isoformat() if b.borrow_date else "",
                "returnDeadline": b.return_deadline.isoformat() if b.return_deadline else "",
            }
        )
    return JsonResponse({"books": payload})


@csrf_exempt
@require_GET
def api_admin_book_get(request, book_id: int):
    _, err = _require_admin(request)
    if err:
        return err
    book = Book.objects.filter(id=book_id).first()
    if not book:
        return JsonResponse({"error": "Not found"}, status=404)
    return JsonResponse(
        {
            "book": {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "category": book.shelf_category,
                "description": book.description,
            }
        }
    )


@csrf_exempt
@require_GET
def api_admin_books(request):
    _, err = _require_admin(request)
    if err:
        return err
    books = Book.objects.all()
    return JsonResponse({"books": [_book_admin_row(b) for b in books]})


@csrf_exempt
@require_http_methods(["POST"])
def api_admin_book_create(request):
    _, err = _require_admin(request)
    if err:
        return err

    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    title = (data.get("title") or "").strip()
    author = (data.get("author") or "").strip()
    description = (data.get("description") or "").strip()
    shelf_category = (data.get("category") or "").strip()

    if not title or not author or not shelf_category or not description:
        return JsonResponse({"error": "Missing required fields"}, status=400)

    base = slugify(title)[:50] or "book"
    slug = base
    n = 2
    while Book.objects.filter(slug=slug).exists():
        slug = f"{base}-{n}"
        n += 1

    book = Book.objects.create(
        slug=slug,
        external_id=None,
        title=title,
        author=author,
        description=description,
        shelf_category=shelf_category,
        tags=[shelf_category.lower()],
        status=Book.STATUS_AVAILABLE,
    )
    return JsonResponse({"ok": True, "book": _book_admin_row(book)})


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def api_admin_book_update(request, book_id: int):
    _, err = _require_admin(request)
    if err:
        return err

    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    book = Book.objects.filter(id=book_id).first()
    if not book:
        return JsonResponse({"error": "Not found"}, status=404)

    title = (data.get("title") or book.title).strip()
    author = (data.get("author") or book.author).strip()
    description = (data.get("description") or book.description).strip()
    shelf_category = (data.get("category") or book.shelf_category or "").strip()

    book.title = title
    book.author = author
    book.description = description
    book.shelf_category = shelf_category
    if shelf_category:
        book.tags = [shelf_category.lower()]
    book.save()
    return JsonResponse({"ok": True, "book": _book_admin_row(book)})


@csrf_exempt
@require_http_methods(["DELETE"])
def api_admin_book_delete(request, book_id: int):
    _, err = _require_admin(request)
    if err:
        return err

    book = Book.objects.filter(id=book_id).first()
    if not book:
        return JsonResponse({"error": "Not found"}, status=404)
    book.delete()
    return JsonResponse({"ok": True})
