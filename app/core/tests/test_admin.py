"""Test for django admin modifications"""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Test for the Django Admin Site"""

    def setUp(self):
        """Create User and Client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="testAdmin2@example.com", password="admin2password"
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testPassword", name="Test User"
        )

    def test_users_list(self):
        """Test that users are listed on the page"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the user edit page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the user create page works"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
