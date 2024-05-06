"""TESTS FOR THE USER API"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    """CREATE AND RETURN A NEW USER"""
    return get_user_model().objects.create(**params)


class PublicUserApiTests(TestCase):
    """TEST THE PUBLIC FEATURES OF THE USER API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating user with valid payload is successful"""

        payload = {
            "email": "test@mail.com",
            "password": "test123",
            "name": "Test Name",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn(
            "password", res.data
        )  # Make sure the users password is no returned

    def test_user_with_email_exists_error(self):
        """TESTS IF USER EXISTS"""
        payload = {
            "email": "test@mail.com",
            "password": "test123",
            "name": "Test Name",
        }

        create_user(**payload)  # The ** is like the spread operator in JS ...
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # If the user exists THROW bad request

    def test_password_too_short_error(self):
        """TESTS IF PASSWORD IS TOO SHORT => Password less than 6 Characters"""
        payload = {
            "email": "test@mail.com",
            "password": "pw",
            "name": "Test Name",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """TEST CREATING TOKEN FOR USER"""
        user_details = {
            "name": "Test Name",
            "email": "test@mail.com",
            "password": "test-user-password123",
        }

        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK),

    def test_create_token_bad_credentials(self):
        """TEST RETURNS ERROR IF CREDENTIALS ARE INVALID"""

        create_user(email="mail@admin.com", password="goodPassword123")

        payload = {
            "email": "mail@admin.com",
            "password": "badPassword",
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """TEST POSTING A BLANK PASSWORD"""

        payload = {
            "email": "mail@admin.com",
            "password": "",
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
