from django.urls import path
from .views import SignupView, CustomLoginView, CreatePostView, PostUpdateView, DeletePostView,LikePostView,UnlikePostView,UserPostListView,CommentListCreateAPIView,CommentReplyListCreateAPIView

urlpatterns = [
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