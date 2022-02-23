"""
<h1>Add a new color</h1>

<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
</form>
"""

from demo.models import Color
from django import forms
from django.shortcuts import redirect
from django.template.defaultfilters import slugify
from file_router import render_str


class ColorAddForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ("name", "code")

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Color.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Name already taken!")
        return name

    def save(self, commit=True):
        self.instance.slug = slugify(self.instance.name)
        return super().save(commit)


def view(request):
    form = ColorAddForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        color = form.save()
        return redirect("colors_slug", color.slug)
    return render_str(__doc__, request, {"form": form})
