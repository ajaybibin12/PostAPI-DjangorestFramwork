from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Like,Comment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile','password']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        # Override the validate method to include custom behavior if needed
        data = super().validate(attrs)
        data.update({'username': self.user.username})
        return data

# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ['id', 'content', 'author', 'created_at', 'parent']
#         ref_name = 'CommentSerializer'
class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    author = serializers.StringRelatedField()
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'parent', 'replies']
        ref_name = 'CommentSerializer'

    def get_replies(self, obj):
        # Get replies to this comment
        replies = Comment.objects.filter(parent=obj)
        return CommentSerializer(replies, many=True).data
    
class PostSerializer(serializers.ModelSerializer):
    tagged_users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)
    like_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'date_created', 'published', 'author', 'tagged_users','like_count','comments']
        ref_name = 'PostSerializer'

    def get_like_count(self, obj):
        return Like.objects.filter(post=obj).count()
    
    def create(self, validated_data):
        tagged_users = validated_data.pop('tagged_users', [])
        post = Post.objects.create(**validated_data)
        post.tagged_users.set(tagged_users)
        return post
    def update(self, instance, validated_data):
        request=self.context.get('request')
        if request.user != instance.author:
            raise serializers.ValidationError('You are not authorized to update this post')
        return super().update(instance, validated_data)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post']
        ref_name = 'LikeSerializer'

