import pytest
from django.urls import NoReverseMatch, reverse

from demo.models import Color


@pytest.fixture
def color():
    return Color.objects.create(name="Foo Color", slug="foo", code="00ff00")


def test_not_a_view(client):
    with pytest.raises(NoReverseMatch):
        reverse("not_a_view")

    response = client.get("/not-a-view")
    assert response.status_code == 404


def test_append_slash(settings):
    settings.ROOT_URLCONF = "demo.urls_with_slash"
    assert reverse("home") == "/"
    assert reverse("colors") == "/colors/"
    assert reverse("colors_add") == "/colors/add/"
    assert reverse("colors_slug", args=["abc"]) == "/colors/abc/"


def test_home(client):
    url = reverse("home")
    assert (
        url == "/"
    ), "Expected the file `views/__init__.py` to produce the url `/` with the name `home`"

    response = client.get(url)
    assert response.status_code == 200


def test_current_time(client):
    url = reverse("current_time")
    assert (
        url == "/current-time"
    ), "Expected the file `views/current-time.py` to produce the url `/current-time` with the name `current_time`"

    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_colors(client, color):
    url = reverse("colors")
    assert (
        url == "/colors"
    ), "Expected the file `views/colors/__init__.py` to produce the url `/colors` with the name `colors`"

    response = client.get(url)
    assert response.status_code == 200
    assert color.name in str(response.content)


@pytest.mark.django_db
def test_colors_slug(client, color):
    url = reverse("colors_slug", args=[color.slug])
    assert (
        url == "/colors/foo"
    ), "Expected the file `views/colors/<slug:slug>.py` to produce the url `/colors/<slug:slug>` with the name `colors_slug`"

    response = client.get(url)
    assert response.status_code == 200
    assert color.name in str(response.content)
    assert color.code in str(response.content)


@pytest.mark.django_db
class TestColorsAdd:
    def test_get(self, client):
        url = reverse("colors_add")
        assert (
            url == "/colors/add"
        ), "Expected the file `views/colors/add.py` to produce the url `/colors/add` with the name `colors_add`"

        response = client.get(url)
        assert response.status_code == 200
        assert b'<input type="text" name="name"' in response.content
        assert b'<input type="text" name="code"' in response.content

    def test_post(self, client):
        url = reverse("colors_add")

        response = client.post(url, data={"name": "Red", "code": "ff0000"})

        assert response.status_code == 302
        assert Color.objects.filter(name="Red", code="ff0000", slug="red").exists()

    def test_post__duplicate_name(self, client, color):
        url = reverse("colors_add")

        response = client.post(url, data={"name": color.name, "code": "ff0000"})

        assert response.status_code == 200
        assert b"Name already taken!" in response.content
        assert Color.objects.count() == 1
