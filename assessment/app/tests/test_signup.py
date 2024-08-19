# app/tests/test_signup.py

from rest_framework import status
from app.tests.base import BaseTest
from django.urls import reverse

class SignupTestCase(BaseTest):
    def test_user_can_signup(self):
        data = {
            "username": "newuser",
            "password": "New@Password123",
            "email": "newuser@example.com",
            "mobile": "1234567890"
        }
        response = self.client.post(reverse('signup'), data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
