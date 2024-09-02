from django.urls import path
from .views import SignupView, CustomLoginView, CreatePostView, PostUpdateView, DeletePostView,LikePostView,UnlikePostView,UserPostListView,CommentListCreateAPIView,CommentReplyListCreateAPIView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication


schema_view = get_schema_view(
    openapi.Info(
        title="Post API",
        default_version='v1',
        description="this api handles create posts and publish,like,unlike and delete posts",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ajaybibin12@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(JWTAuthentication,),
)
urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('create_posts/', CreatePostView.as_view(), name='create-post'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', DeletePostView.as_view(), name='delete-post'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    path('posts/', UserPostListView.as_view(), name='user-post-list'),
    path('posts/<int:post_id>/comments/', CommentListCreateAPIView.as_view(), name='post-comments'),
    path('comments/<int:comment_id>/replies/', CommentReplyListCreateAPIView.as_view(), name='comment-replies'),
]