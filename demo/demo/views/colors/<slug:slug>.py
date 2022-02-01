"""
<h1>{{ color.name }}</h1>
<p>The code is {{ color.code }}</p>
"""

from demo.models import Color
from django.shortcuts import get_object_or_404
from file_router import render_str


def view(request, slug):
    color = get_object_or_404(Color, slug=slug)
    return render_str(__doc__, request, {"color": color})
