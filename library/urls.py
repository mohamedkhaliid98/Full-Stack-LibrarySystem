from django.urls import path

from . import api

urlpatterns = [
    path("register/", api.api_register),
    path("login/", api.api_login),
    path("logout/", api.api_logout),
    path("me/", api.api_me),
    path("books/", api.api_books_list),
    path("books/<slug:slug>/", api.api_book_detail),
    path("books/<slug:slug>/borrow/", api.api_book_borrow),
    path("books/<slug:slug>/return/", api.api_book_return),
    path("borrowed/", api.api_borrowed_list),
    path("admin/books/<int:book_id>/detail/", api.api_admin_book_get),
    path("admin/books/", api.api_admin_books),
    path("admin/books/create/", api.api_admin_book_create),
    path("admin/books/<int:book_id>/delete/", api.api_admin_book_delete),
    path("admin/books/<int:book_id>/", api.api_admin_book_update),
]
