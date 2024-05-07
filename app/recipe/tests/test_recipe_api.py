"""Test for the recipe APIs

"""

from decimal import Decimal

from core.models import Recipe
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import RecipeSerializer
from rest_framework import status
from rest_framework.test import APIClient

RECIPE_URL = reverse("recipe:recipe-list")


def create_recipe(user, **params):
    """Create and return a new sample recipe"""

    defaults = {
        "title": "Sample Test Recipe",
        "time_minutes": 10,
        "price": Decimal("5.00"),
        "description": "Sample Test Recipe",
        "link": "http://example.com/sample.pdf",
    }

    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeApiTests(TestCase):
    """Test the publicly available recipe API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test the authorized recipe API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass123",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by("-id")

        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test that list of recipes is limited to the authenticated user"""

        other_user = get_user_model().objects.create_user(
            email="test2@example.com",
            password="testpass123",
        )

        create_recipe(user=self.user)
        create_recipe(user=other_user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
