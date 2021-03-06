from core.models import Ingredient
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsAPITests(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITests(TestCase):
    """Test private ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'password'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving list of ingredients"""

        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')
        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that only authenticated user's ingredients are returned"""

        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'otherpass'
        )

        Ingredient.objects.create(user=user2, name='Vinegar')
        new_ingredient = Ingredient.objects.create(user=self.user,
                                                   name='Tumeric')
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], new_ingredient.name)

    def test_create_ingredient_successful(self):
        """Test create a new ingredient"""

        info = {'name': 'Cabbage'}
        self.client.post(INGREDIENTS_URL, info)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=info['name']
        )

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test creating ingredient with invalid info"""

        info = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, info)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
