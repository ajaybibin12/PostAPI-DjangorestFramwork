# app/tests/test_post.py

from rest_framework import status
from .base import BaseTest
from django.urls import reverse

class PostTestCase(BaseTest):
    def test_user_can_create_post(self):
        data = {
            "title": "My First Post",
            "description": "This is the content of the post.",
            "published": True,
            "author": self.user.id
        }
        response = self.client.post(reverse('create-post'), data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "My First Post")

