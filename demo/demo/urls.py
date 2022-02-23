from django.contrib import admin
from django.urls import path

from file_router import file_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    *file_patterns("demo/views"),
]
