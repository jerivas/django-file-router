from django.contrib import admin
from django.db import models


class Color(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    code = models.CharField(max_length=8)

    def __str__(self):  # pragma: nocover
        return self.name


admin.site.register(Color)
