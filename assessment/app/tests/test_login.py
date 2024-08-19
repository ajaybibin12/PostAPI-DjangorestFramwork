# app/tests/test_login.py

from rest_framework import status
from .base import BaseTest
from django.urls import reverse

class LoginTestCase(BaseTest):
    def test_user_can_login(self):
        data = {
            "username": "testuser",
            "password": "TestPassword123"
        }
        response = self.client.post(reverse('login'), data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
