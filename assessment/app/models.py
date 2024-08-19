# app/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    mobile = models.CharField(max_length=20, null=False)
    # Other fields like email, username, and password are inherited from AbstractUser

class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    tagged_users = models.ManyToManyField(User, related_name='tagged_posts', through='Tag')

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
