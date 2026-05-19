from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    ROLE_ADMIN = "admin"
    ROLE_USER = "user"
    ROLE_CHOICES = ((ROLE_ADMIN, "admin"), (ROLE_USER, "user"))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="library_profile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)

    def __str__(self):
        return f"{self.user.email} ({self.role})"


class Book(models.Model):
    STATUS_AVAILABLE = "Available"
    STATUS_BORROWED = "Borrowed"
    STATUS_CHOICES = (
        (STATUS_AVAILABLE, STATUS_AVAILABLE),
        (STATUS_BORROWED, STATUS_BORROWED),
    )

    slug = models.SlugField(max_length=64, unique=True)
    external_id = models.PositiveIntegerField(null=True, blank=True, help_text="Optional ID from admin add-book form.")
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    shelf_category = models.CharField(max_length=100, blank=True, help_text="Admin shelf category label.")
    tags = models.JSONField(default=list, blank=True, help_text="Lower-case tags for user search filters.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
    borrowed_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="borrowed_books"
    )
    borrow_date = models.DateField(null=True, blank=True)
    return_deadline = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title
