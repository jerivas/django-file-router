"""
<h1>Hello 👋</h1>

<p>Here are some links:</p>
<ul>
    <li><a href="{% url 'colors' %}">Colors</a></li>
    <li><a href="{% url 'current-time' %}">Current Time</a></li>
</ul>
"""

from file_router import render_str


def view(request):
    return render_str(__doc__, request)
