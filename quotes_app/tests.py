"""
Test cases for the 'quotes_app' app.
"""
from django.test import TestCase, Client
from django.urls import reverse
from .models import Author, Tag, Quote
from django.contrib.auth.models import User
from .templatetags.quote_tags import top_tags

class AuthorModelTest(TestCase):
    """
    Test cases for the Author model.
    """

    def setUp(self):
        """
        Set up a test author for testing.
        """
        self.author = Author.objects.create(
            name="Test Author",
            description="Test Description",
            born_date="01-01-2000",
            born_location="Test Location",
            user=User.objects.create_user(username="testuser")
        )

    def test_author_str(self):
        """
        Test the string representation of the Author model.
        """
        self.assertEqual(str(self.author), "Test Author")

class TagModelTest(TestCase):
    """
    Test cases for the Tag model.
    """

    def setUp(self):
        """
        Set up a test tag for testing.
        """
        self.tag = Tag.objects.create(
            name="Test Tag",
            user=User.objects.create_user(username="testuser")
        )

    def test_tag_str(self):
        """
        Test the string representation of the Tag model.
        """
        self.assertEqual(str(self.tag), "Test Tag")

class QuoteModelTest(TestCase):
    """
    Test cases for the Quote model.
    """

    def setUp(self):
        """
        Set up a test quote with an author and tag for testing.
        """
        self.author = Author.objects.create(
            name="Test Author",
            description="Test Description",
            born_date="01-01-2000",
            born_location="Test Location",
            user=User.objects.create_user(username="testuser")
        )
        self.tag = Tag.objects.create(
            name="Test Tag",
            user=self.author.user
        )
        self.quote = Quote.objects.create(
            text="Test Quote",
            author=self.author,
            user=self.author.user
        )
        self.quote.tags.add(self.tag)

    def test_quote_creation(self):
        """
        Test the creation of a Quote instance.
        """
        self.assertEqual(self.quote.text, "Test Quote")
        self.assertEqual(self.quote.author, self.author)
        self.assertIn(self.tag, self.quote.tags.all())

class ViewsTest(TestCase):
    """
    Test cases for views in the 'quotes_app'.
    """

    def setUp(self):
        """
        Set up a test client, user, author, tag, and quote for testing views.
        """
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.author = Author.objects.create(
            name="Test Author",
            description="Test Description",
            born_date="01-01-2000",
            born_location="Test Location",
            user=self.user
        )
        self.tag = Tag.objects.create(
            name="Test Tag",
            user=self.user
        )
        self.quote = Quote.objects.create(
            text="Test Quote",
            author=self.author,
            user=self.user
        )
        self.quote.tags.add(self.tag)

    def test_main_view(self):
        """
        Test the main view renders correctly.
        """
        response = self.client.get(reverse("quotes_app:main"))
        self.assertEqual(response.status_code, 200)

    def test_author_details_view(self):
        """
        Test the author details view renders correctly.
        """
        response = self.client.get(reverse("quotes_app:author_details", args=[self.author.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.name)

    def test_tag_details_view(self):
        """
        Test the tag details view renders correctly.
        """
        response = self.client.get(reverse("quotes_app:tag_details", args=[self.tag.name]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tag.name)

    def test_quote_details_view(self):
        """
        Test the quote details view renders correctly.
        """
        response = self.client.get(reverse("quotes_app:quote_details", args=[self.quote.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.quote.text)

class TemplateTagsTest(TestCase):
    """
    Test cases for custom template tags in the 'quotes_app'.
    """

    def setUp(self):
        """
        Set up test tags and quotes for testing the 'top_tags' template tag.
        """
        self.user = User.objects.create_user(username="testuser")
        self.tag1 = Tag.objects.create(name="Tag1", user=self.user)
        self.tag2 = Tag.objects.create(name="Tag2", user=self.user)
        self.quote1 = Quote.objects.create(text="Quote1", author=Author.objects.create(
            name="Author1", description="Desc", born_date="01-01-2000", born_location="Loc", user=self.user), user=self.user)
        self.quote2 = Quote.objects.create(text="Quote2", author=Author.objects.create(
            name="Author2", description="Desc", born_date="01-01-2000", born_location="Loc", user=self.user), user=self.user)
        self.quote1.tags.add(self.tag1)
        self.quote2.tags.add(self.tag2)

    def test_top_tags(self):
        """
        Test the 'top_tags' template tag returns the correct tags and sizes.
        """
        result = top_tags()
        self.assertEqual(len(result), 2)
        self.assertIn((self.tag1, 15), result)
        self.assertIn((self.tag2, 15), result)
