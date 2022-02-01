import os
import re
from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.urls import path

__version__ = "9999dev0"  # Managed by semantic-release, do not edit


def file_patterns(start_dir, append_slash=False):
    """
    Create urlpatterns from a directory structure
    """
    patterns = []
    start_dir_re = re.compile(f"^{start_dir}")
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if not file.endswith(".py"):
                continue
            module_path = f"{root}/{file}".replace(".py", "").replace("/", ".")
            try:
                module = import_module(module_path)
            except ImportError as exc:
                raise ImproperlyConfigured(
                    f"Failed to import {module_path}. Ensure it's a valid Python file."
                ) from exc
            view_fn = getattr(module, "view", None)
            if not callable(view_fn):
                continue
            url = "" if file == "index.py" else file.replace(".py", "")
            url = start_dir_re.sub("", f"{root}/{url}").strip("/")
            url = (url + "/") if append_slash else url
            patterns.append(path(url, view_fn))
    return patterns


def render_str(source, request, context=None):
    """
    Take
    """
    rendered = Template(source).render(RequestContext(request, context))
    return HttpResponse(rendered)
