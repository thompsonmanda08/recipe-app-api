"""Views for the recipe APIs for"""

from core.models import Recipe
from recipe import serializers
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class RecipeViewSet(viewsets.ModelViewSet):
    """View for managing recipe APIs"""

    serializer_class = serializers.RecipeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)
