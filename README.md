# django-file-router

File and folder-based routes for Django views.

## Installation

```
pip install django-file-router
```

## The problem

Imagine you are creating a Django project with some CRUD views for your objects. How many files do you need to allow users to create a new object?

1. Create a form class in `forms.py`
2. Create a view function that imports the form in `views.py`
3. Create an HTML template that's referenced by the view somewhere in a `templates` directory
4. Edit `urls.py` to add your new view function

That's a total of four files to accomplish something that to end users appears as a single action (add an object). On top of that you need to come up with a name for the form, the view, the template, and the url pattern even if they end up being some variation of `add_:object class:`.

## The solution

Inspired by the popular JS frameworks like Next.js and Remix and the old-school convenience of PHP, `django-file-router` allows developers to store all form, template, and view code in a single file; while also inferring the appropriate URL patterns from the directory structure of these views.

In practice it looks like this:

```python
"""
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
</form>
"""

from django import forms
from django.shortcuts import redirect
from file_router import render_str

from myapp.models import MyModel

class AddMyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ("name", "description")

def view(request):
    form = AddMyModelForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save()
        return redirect(obj.get_absolute_url())
    return render_str(__doc__, request, {"form": form})
```

There's very little magic in this file. The template is stored at the top as a regular Python docstring and is later passed to the special function `render_str` at the bottom of the file. This function is identical to Django's `render` shortcut with the difference that the template code is passed directly as a string instead of a path. The only other hard requirement is that the file must expose a callable named `view` that accepts the request and returns a response.

You would store this code in a file like `myapp/views/mymodel/add.py` and add this to your `urls.py`:

```python
from file_router import file_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    *file_patterns("myapp/views"),
]
```

With that single call to `file_patterns` the function will generate URL patterns for all your views automatically based on their folder structure inside `myapp/views`. For the file we created earlier at `myapp/views/mymodel/add.py` this will result in a url of `/mymodel/add`. Then by simply creating more files and folders the URL patterns will be updated without any manual input.

Here's an example folder structure for a complete CRUD workflow for `MyModel`:

```
myapp
└── views
    └── mymodel
        ├── <id>
        │   ├── delete.py
        │   ├── edit.py
        │   └── index.py
        ├── add.py
        └── index.py

3 directories, 5 files
```

This would generate the following URL patterns:

- `/mymodel`: list of all instances
- `/mymodel/add`: add a new instance
- `/mymodel/<id>`: view instance
- `/mymodel/<id>/edit`: edit instance
- `/mymodel/<id>/delete`: delete instance

Each file now holds all the pieces required to perform a given action and requires much less context switching.

Notice that special placeholders like `<id>` are parsed as expected by Django's [`path`](https://docs.djangoproject.com/en/4.0/topics/http/urls/#how-django-processes-a-request) function, which means you can use path converters by including them in file and folder names such as `<int:id>`. For example, to get a single instance enforcing an integer `id` create a file `myapp/views/mymodel/<int:id>/index.py` with the code:

```python
"""
<h1>{{ obj.name }}</h1>
"""

from django.shortcuts import get_object_or_404
from file_router import render_str

from myapp.models import MyModel

def view(request, id):
    obj = get_object_or_404(MyModel, id=id)
    return render_str(__doc__, request, {"obj": obj})
```

More examples are available in the [demo folder](https://github.com/jerivas/django-file-router/tree/main/demo).

## FAQ

### What about separation of concerns?

I think that depends on how you define concerns. If you want to keep view, form, and template code separate then this approach goes against that, but in return you keep all code related to a particular user-facing functionality together, which is easier to reason about as this is how features are developed and maintained.

### What about syntax highlighting for the template code?

Yes, currently template code is just a plain string, but I'm sure there's a way to create a custom language mode in IDEs that will highlight it as expected. I've seen it work in single file Vue components and GraphQL code in JS, so I know it's possible.

### What about named URL patterns?

Every url pattern will also have an auto-generated url name. For example:

| URL                    | URL name            |
|------------------------|---------------------|
| `/mymodel`             | `mymodel`           |
| `/mymodel/add`         | `mymodel-add`       |
| `/mymodel/<id>`        | `mymodel-id`        |
| `/mymodel/<id>/edit`   | `mymodel-id-edit`   |
| `/mymodel/<id>/delete` | `mymodel-id-delete` |

### Are you serious?

Yes, kinda? This seems like a net positive gain in productivity and also reduces cognitive load, plus it's a pattern that's been tried and tested for years. It's also very light and doesn't require too much magic. So I plan to use it where I can and see if others show interest.
