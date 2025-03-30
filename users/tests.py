from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.profile = Profile.objects.get(user=self.user)

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.avatar.name, "default_avatar.jpg")

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_signup_view(self):
        response = self.client.get(reverse("users:signup"))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_authenticated(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_unauthenticated(self):
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 302)  # Redirect to login
