"""
The current datetime is {% now "DATETIME_FORMAT" %}
"""

from file_router import render_str


def view(request):
    return render_str(__doc__, request)
