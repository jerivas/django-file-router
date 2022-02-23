"""
<h1>Here's a list of all colors</h1>

<ul>
    {% for color in colors %}
        <li><a href="{% url 'colors_slug' color.slug %}">{{ color.name }}</a></li>
    {% endfor %}
</ul>

<p><a href="{% url 'colors_add' %}">Add a new color</a></p>
"""

from demo.models import Color
from file_router import render_str


def view(request):
    colors = Color.objects.all()
    return render_str(__doc__, request, {"colors": colors})
