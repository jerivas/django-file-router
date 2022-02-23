"""Same as urls.py, but with `append_slash=True`"""

from django.contrib import admin
from django.urls import path

from file_router import file_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    *file_patterns("demo/views", append_slash=True),
]
