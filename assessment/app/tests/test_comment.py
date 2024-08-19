# app/tests/test_comment.py

from rest_framework import status
from .base import BaseTest
from app.models import Post
from django.urls import reverse

class CommentTestCase(BaseTest):
    def setUp(self):
        super().setUp()
        self.post = Post.objects.create(
            title="Test Post", description="Test Description", author=self.user, published=True
        )

    def test_user_can_comment_on_post(self):
        data = {
            "content": "This is a comment.",
            "post": self.post.id
        }
        response = self.client.post(reverse('post-comments', kwargs={'post_id': self.post.id}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], "This is a comment.")
