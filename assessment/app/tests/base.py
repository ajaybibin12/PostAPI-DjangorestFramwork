# app/tests/base.py

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from app.models import User

class BaseTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='TestPassword123')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def create_user(self, username='user1', password='TestPassword123', email='user1@example.com'):
        return User.objects.create_user(username=username, password=password, email=email)

