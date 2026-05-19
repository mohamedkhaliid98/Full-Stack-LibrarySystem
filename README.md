# Online Library — Django backend

This project serves the **Online Library System** static frontend (ported from [silent-spark/project-1-web](https://github.com/silent-spark/project-1-web)) and exposes JSON APIs under `/api/` so books, borrowing, and accounts are stored in SQLite instead of `localStorage`.

## Quick start

```bash
cd library_django
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_library
python manage.py createsuperuser
python manage.py runserver
```

Open **http://127.0.0.1:8000/**

- Register a normal **User** or **Admin** from **Sign Up**, or use Django admin at `/admin/` after `createsuperuser`.
- Demo books (`cpp`, `clean`, `alg`) are created by `seed_library` if missing.

## API (JSON, session cookie)

| Method | Path | Notes |
|--------|------|--------|
| POST | `/api/register/` | `{ fullName, email, password, role }` |
| POST | `/api/login/` | `{ email, password }` |
| POST | `/api/logout/` | |
| GET | `/api/me/` | Current user or 401 |
| GET | `/api/books/` | List books (auth) |
| GET | `/api/books/<slug>/` | Detail |
| POST | `/api/books/<slug>/borrow/` | Borrow (auth) |
| POST | `/api/books/<slug>/return/` | Return (owner or admin) |
| GET | `/api/borrowed/` | Current user’s borrowed books |
| GET | `/api/admin/books/` | Admin |
| GET | `/api/admin/books/<id>/detail/` | Admin edit form |
| POST | `/api/admin/books/create/` | Admin add |
| PUT | `/api/admin/books/<id>/` | Admin update |
| DELETE | `/api/admin/books/<id>/delete/` | Admin delete |

> Note: API views use `@csrf_exempt` for simplicity with plain `fetch` from static HTML. For production, prefer CSRF tokens or token auth.

## Layout

- `online_library/` — project settings
- `library/` — models (`Book`, `Profile`), API, migrations, `seed_library` command
- `frontend/` — HTML, `css/`, `js/`, optional `images/` (see `frontend/images/README.txt`)
