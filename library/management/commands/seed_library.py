from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from library.models import Book, Profile


class Command(BaseCommand):
    help = "Create demo books and ensure admin profiles exist."

    def handle(self, *args, **options):
        demo_books = [
            {
                "slug": "cpp",
                "title": "C++ How to Program",
                "author": "Deitel & Deitel",
                "description": (
                    "A comprehensive guide to C++ programming. It uses a live-code approach to teach "
                    "object-oriented programming to university students."
                ),
                "shelf_category": "Programming",
                "tags": ["programming", "coding"],
            },
            {
                "slug": "clean",
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "description": "A handbook of agile software craftsmanship with practical advice for writing maintainable code.",
                "shelf_category": "Software Engineering",
                "tags": ["coding"],
            },
            {
                "slug": "alg",
                "title": "Introduction to Algorithms",
                "author": "CLRS",
                "description": "Foundational algorithms and data structures used in computer science and engineering.",
                "shelf_category": "Algorithms",
                "tags": ["technology", "programming"],
            },
        ]

        for row in demo_books:
            book, created = Book.objects.get_or_create(
                slug=row["slug"],
                defaults={
                    "title": row["title"],
                    "author": row["author"],
                    "description": row["description"],
                    "shelf_category": row["shelf_category"],
                    "tags": row["tags"],
                    "status": Book.STATUS_AVAILABLE,
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created book: {book.title}"))
            else:
                self.stdout.write(f"Book already exists: {book.title}")

        for user in User.objects.all():
            Profile.objects.get_or_create(
                user=user,
                defaults={"role": Profile.ROLE_ADMIN if user.is_superuser else Profile.ROLE_USER},
            )

        self.stdout.write(self.style.SUCCESS("Done. Run the server and open http://127.0.0.1:8000/"))
