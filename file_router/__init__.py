import os
import re
from importlib import import_module

from django.http import HttpResponse
from django.template import RequestContext, Template
from django.urls import path

__version__ = "0.2.0"

DISALLOWED_CHARS = re.compile(
    "|".join(
        [
            r"^-+",  # Leading dashes
            r"[<>]",  # Angle brackets (url param wrapper)
            r"\w+\:",  # Letters followed by colon (path converters)
            r"-+$",  # Trailing dashes
        ]
    )
)
TO_DASHES = re.compile("[/_]")  # Match slash and underscore


def file_patterns(start_dir, append_slash=False):
    """
    Create urlpatterns from a directory structure
    """
    patterns = []
    start_dir_re = re.compile(f"^{start_dir}")
    for root, dirs, files in os.walk(start_dir):
        # Reverse the list so files that start with "<" go to the bottom and
        # regular files come to the top. This ensures hard-coded url params
        # always match before variable ones
        files = tuple(reversed(files))
        for file in files:
            if not file.endswith(".py"):
                continue

            module_path = f"{root}/{file}".replace(".py", "").replace("/", ".")
            module = import_module(module_path)
            view_fn = getattr(module, "view", None)
            if not callable(view_fn):
                continue

            try:
                url = view_fn.url
            except AttributeError:
                url = "" if file == "index.py" else file.replace(".py", "")
                url = start_dir_re.sub("", f"{root}/{url}").strip("/")
                url = (url + "/") if append_slash else url

            try:
                urlname = view_fn.urlname
            except AttributeError:
                urlname = DISALLOWED_CHARS.sub("", TO_DASHES.sub("-", url))

            patterns.append(path(url, view_fn, name=urlname))
    return patterns


def render_str(source, request, context=None):
    """
    Take a string and respond with a fully rendered template
    """
    rendered = Template(source).render(RequestContext(request, context))
    return HttpResponse(rendered)
