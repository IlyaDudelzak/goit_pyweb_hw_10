import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyweb_hw_10.settings')  # Replace with your settings file path
django.setup()

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from quotes_app.models import Author, Tag, Quote
from quotes_app.forms import AuthorForm, TagForm, QuoteForm
from unittest.mock import patch



@pytest.fixture
def test_user(django_user_model):
    """
    Fixture to create a test user.
    """
    user = django_user_model.objects.create_user(
        username="testuser", password="testpassword"
    )
    return user

@pytest.fixture
def authenticated_client(client, test_user):
    """
    Fixture to create an authenticated client.
    """
    client.force_login(test_user)
    return client

@pytest.mark.django_db
def test_author_create_view(authenticated_client):
    """
    Test the author create view.
    """
    url = reverse("quotes_app:author_create")
    data = {"name": "Test Author", "born_date": "1900-01-01", "born_location": "Test Location", "description": "Test Description"}
    response = authenticated_client.post(url, data)
    assert response.status_code == 302  # Redirect after successful creation
    assert Author.objects.filter(name="Test Author").exists()

@pytest.mark.django_db
def test_tag_create_view(authenticated_client):
    """
    Test the tag create view.
    """
    url = reverse("quotes_app:tag_create")
    data = {"name": "Test Tag"}
    response = authenticated_client.post(url, data)
    assert response.status_code == 302  # Redirect after successful creation
    assert Tag.objects.filter(name="Test Tag").exists()

@pytest.mark.django_db
def test_quote_create_view(authenticated_client, test_user):
    """
    Test the quote create view.
    """
    author = Author.objects.create(name="Test Author", born_date="1900-01-01", born_location="Test Location", description="Test Description")
    tag = Tag.objects.create(name="Test Tag")
    url = reverse("quotes_app:quote_create")
    data = {"text": "Test Quote", "author": author.id, "tags": [tag.id]}
    response = authenticated_client.post(url, data)
    assert response.status_code == 302  # Redirect after successful creation
    assert Quote.objects.filter(text="Test Quote").exists()

@pytest.mark.django_db
def test_author_details_view(client):
    """
    Test the author details view.
    """
    author = Author.objects.create(name="Test Author", born_date="1900-01-01", born_location="Test Location", description="Test Description")
    url = reverse("quotes_app:author_details", kwargs={"id": author.id})
    response = client.get(url)
    assert response.status_code == 200
    assert "Test Author" in response.content.decode()

@pytest.mark.django_db
def test_tag_details_view(client):
    """
    Test the tag details view.
    """
    tag = Tag.objects.create(name="Test Tag")
    url = reverse("quotes_app:tag_details", kwargs={"tag": tag.name})
    response = client.get(url)
    assert response.status_code == 200
    assert "Test Tag" in response.content.decode()

@pytest.mark.django_db
def test_quote_details_view(client):
    """
    Test the quote details view.
    """
    author = Author.objects.create(name="Test Author", born_date="1900-01-01", born_location="Test Location", description="Test Description")
    quote = Quote.objects.create(text="Test Quote", author=author)
    url = reverse("quotes_app:quote_details", kwargs={"id": quote.id})
    response = client.get(url)
    assert response.status_code == 200
    assert "Test Quote" in response.content.decode()

@pytest.mark.django_db
def test_main_view(client):
    """
    Test the main view.
    """
    url = reverse("quotes_app:main")
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_author_page_view(client):
    """
    Test the author page view.
    """
    url = reverse("quotes_app:author_page", kwargs={"page": 1})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_tag_page_view(client):
    """
    Test the tag page view.
    """
    url = reverse("quotes_app:tag_page", kwargs={"page": 1})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_quote_page_view(client):
    """
    Test the quote page view.
    """
    url = reverse("quotes_app:quote_page", kwargs={"page": 1})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
@patch('quotes_app.views.requests.get')
def test_parse_quotes_view(mock_get, authenticated_client, test_user):
    """
    Test the parse quotes view.
    """
    # Mock the requests.get to avoid external calls
    mock_get.return_value.text = "<html><body><div class='quote'><span class='text'>Test Quote</span><small class='author'>Test Author</small><a class='tag'>Test Tag</a></div></body></html>"
    url = reverse("quotes_app:parse_quotes")
    response = authenticated_client.get(url)
    assert response.status_code == 302  # Redirect after parsing
    assert Quote.objects.filter(text="Test Quote").exists()
