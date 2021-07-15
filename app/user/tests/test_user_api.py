from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    """Test the users API (non authenticated)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid info is successful"""

        info = {
            'email': 'test@gmail.com',
            'password': 'password',
            'name': 'Joe Joe'
        }

        res = self.client.post(CREATE_USER_URL, info)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(info['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user when the user already exists"""
        info = {
            'email': 'test@gmail.com',
            'password': 'password',
        }

        create_user(**info)
        res = self.client.post(CREATE_USER_URL, info)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short(self):
        """Password must be more than 5 characters"""
        info = {
            'email': 'test@gmail.com',
            'password': 'pa',
        }

        res = self.client.post(CREATE_USER_URL, info)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        user_exists = get_user_model().objects.filter(email = info['email']).exists()

        self.assertFalse(user_exists)
