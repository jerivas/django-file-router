import shutil

import pytest

from . import file_patterns


@pytest.fixture(scope="session", autouse=True)
def copy_views():
    """Copy the views folder of the demo project to this folder"""
    shutil.copytree("demo/demo/views", "views")
    yield
    shutil.rmtree("views")


def test_append_slash():
    patterns = file_patterns("views", append_slash=True, exclude="")
    output = [(str(p.pattern), p.name) for p in patterns]
    assert output == [
        ("current-time/", "current_time"),
        ("colors/add/", "colors_add"),
        ("colors/", "colors"),
        ("colors/<slug:slug>/", "colors_slug"),
        ("", "home"),
    ]


def test_exclude():
    patterns = file_patterns("views", append_slash=False, exclude="*-time.py")
    output = [(str(p.pattern), p.name) for p in patterns]
    assert output == [
        ("colors/add", "colors_add"),
        ("colors", "colors"),
        ("colors/<slug:slug>", "colors_slug"),
        ("", "home"),
    ]
