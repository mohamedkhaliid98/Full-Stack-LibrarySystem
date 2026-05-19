from django.contrib import admin

from .models import Book, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "slug", "status", "borrowed_by")
    search_fields = ("title", "author", "slug")
