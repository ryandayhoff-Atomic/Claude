"""Tests for utility functions."""

from utils import slugify


def test_slugify_basic():
    assert slugify("Hello World") == "hello-world"


def test_slugify_special_characters():
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_extra_whitespace():
    assert slugify("  Hello   World  ") == "hello-world"


def test_slugify_unicode():
    assert slugify("Héllo Wörld") == "hello-world"
    assert slugify("café résumé") == "cafe-resume"
    assert slugify("naïve coöperate") == "naive-cooperate"


def test_slugify_empty_string():
    assert slugify("") == ""


def test_slugify_already_slug():
    assert slugify("hello-world") == "hello-world"
