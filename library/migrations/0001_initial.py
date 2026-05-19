# Generated manually for library app

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(max_length=64, unique=True)),
                ("external_id", models.PositiveIntegerField(blank=True, help_text="Optional ID from admin add-book form.", null=True)),
                ("title", models.CharField(max_length=255)),
                ("author", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("shelf_category", models.CharField(blank=True, help_text="Admin shelf category label.", max_length=100)),
                ("tags", models.JSONField(blank=True, default=list, help_text="Lower-case tags for user search filters.")),
                ("status", models.CharField(choices=[("Available", "Available"), ("Borrowed", "Borrowed")], default="Available", max_length=20)),
                ("borrow_date", models.DateField(blank=True, null=True)),
                ("return_deadline", models.DateField(blank=True, null=True)),
                (
                    "borrowed_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="borrowed_books",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("admin", "admin"), ("user", "user")], default="user", max_length=10)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="library_profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
