from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, CustomTokenObtainPairSerializer,PostSerializer,LikeSerializer,CommentSerializer
from . import serializers
from rest_framework.exceptions import ValidationError
import re
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from .models import Post, Like,Comment


User = get_user_model()

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        if not self.is_password_strong(password):
            raise ValidationError("Password does not meet the minimum strength criteria.")
        serializer.save(password=make_password(password))

    def is_password_strong(self, password):
        # Check minimum length
        if len(password) < 8:
            return False
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False
        
        # Check for at least one digit
        if not re.search(r'\d', password):
            return False
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        
        return True

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     # Limit the queryset to posts authored by the logged-in user
    #     return self.queryset.filter(author=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(author=self.request.user)
        return Post.objects.none() 

    def perform_update(self, serializer):
        # Ensure that only the author can update the post
        post = self.get_object()
        if post.author != self.request.user:
            raise ValidationError("You can only update your own posts.")
        serializer.save()

class DeletePostView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(author=self.request.user)
        return Post.objects.none() 

    def perform_destroy(self, instance):
        # Ensure that only the author can delete the post
        if instance.author != self.request.user:
            raise ValidationError("You can only delete your own posts.")
        instance.delete()


class LikePostView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    queryset= Post.objects.all()

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        post = Post.objects.get(pk=post_id)
        
        # Check if the post is published
        if not post.published:
            return Response({"detail": "You can only like published posts."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the user has already liked the post
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the like
        like = Like(user=request.user, post=post)
        like.save()
        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)
    
class UnlikePostView(generics.DestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    queryset= Post.objects.all()

    def delete(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        post = Post.objects.get(pk=post_id)
        
        # Find the like instance
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"detail": "Post unliked."}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"detail": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)

class UserPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Retrieve the posts created by the logged-in user (both published and unpublished)
        own_posts = Post.objects.filter(author=user)
        # Retrieve published posts created by others
        published_posts_by_others = Post.objects.filter(published=True).exclude(author=user)
        # Combine the two querysets
        return own_posts.union(published_posts_by_others)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id, parent__isnull=True)  # Top-level comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentReplyListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        comment_id = self.kwargs.get('comment_id')
        return Comment.objects.filter(parent_id=comment_id)  # Replies to a specific comment

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)