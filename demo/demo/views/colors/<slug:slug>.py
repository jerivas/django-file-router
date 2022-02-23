"""
<h1>{{ color.name }}</h1>
<p>The code is {{ color.code }}</p>
"""

from django.shortcuts import get_object_or_404

from demo.models import Color
from file_router import render_str


def view(request, slug):
    color = get_object_or_404(Color, slug=slug)
    return render_str(__doc__, request, {"color": color})
