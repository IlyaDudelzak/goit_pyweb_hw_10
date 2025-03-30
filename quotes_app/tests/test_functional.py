import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from quotes_app.models import Author, Tag, Quote

@pytest.mark.django_db
def test_main_route(client):
    """
    Test the main route to ensure it renders correctly.
    """
    response = client.get(reverse("quotes_app:main"))
    assert response.status_code == 200
    assert b"Quotes to GoIT" in response.content

@pytest.mark.django_db
def test_author_details_route(client):
    """
    Test the author details route to ensure it renders correctly.
    """
    user = User.objects.create_user(username="testuser", password="password")
    author = Author.objects.create(
        name="Test Author",
        description="Test Description",
        born_date="01-01-2000",
        born_location="Test Location",
        user=user
    )
    response = client.get(reverse("quotes_app:author_details", args=[author.id]))
    assert response.status_code == 200
    assert b"Test Author" in response.content

@pytest.mark.django_db
def test_tag_details_route(client):
    """
    Test the tag details route to ensure it renders correctly.
    """
    user = User.objects.create_user(username="testuser", password="password")
    tag = Tag.objects.create(name="Test Tag", user=user)
    response = client.get(reverse("quotes_app:tag_details", args=[tag.name]))
    assert response.status_code == 200
    assert b"Test Tag" in response.content

@pytest.mark.django_db
def test_quote_details_route(client):
    """
    Test the quote details route to ensure it renders correctly.
    """
    user = User.objects.create_user(username="testuser", password="password")
    author = Author.objects.create(
        name="Test Author",
        description="Test Description",
        born_date="01-01-2000",
        born_location="Test Location",
        user=user
    )
    quote = Quote.objects.create(text="Test Quote", author=author, user=user)
    response = client.get(reverse("quotes_app:quote_details", args=[quote.id]))
    assert response.status_code == 200
    assert b"Test Quote" in response.content
