from django.urls import re_path

from .frontend import serve_frontend

urlpatterns = [
    re_path(r"^(?P<path>.*)$", serve_frontend),
]
