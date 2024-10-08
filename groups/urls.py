
from django.urls import path
from .views import (
    SearchMaterialByTitleAPIView,
    GroupSearchByTitleAPIView, GroupJoinAPIView, GroupDeleteAPIView, GroupUsersListAPIView,
    GroupUnjoinAPIView, GroupListCreateAPIView, GroupDetailAPIView, GroupBatchUpdateAPIView,
    GroupMaterialCreateAPIView, GroupMaterialListAPIView, GroupMaterialDeleteAPIView,
    UserJoinedGroupsListView,GroupListAPIView
)

from PostsAndComments.views import (
    PostListCreateAPIView,
    PostRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView,
    CommentRetrieveUpdateDestroyAPIView,
    ReplyListCreateAPIView,
    ReplyRetrieveUpdateDestroyAPIView,
    CommentAndReplyListAPIView,
    PostListView, LikePostAPIView, UnLikePostAPIView,
    LikeCommentAPIView, UnLikeCommentAPIView,
    UnLikeReplyAPIView, LikeReplyAPIView
)

urlpatterns = [
    path('', GroupListCreateAPIView.as_view(), name='group-list-create'),
    path('<int:pk>/', GroupDetailAPIView.as_view(), name='group-detail'),
    path('patch_update/<int:pk>/', GroupBatchUpdateAPIView.as_view(), name='group-batch-update'),
    path('delete_patch/<int:pk>/', GroupDeleteAPIView.as_view(), name='group-delete'),
    path('user_joined_groups/', UserJoinedGroupsListView.as_view(), name='user-joined-groups'),
    path('list_groups/', GroupListAPIView.as_view(), name='group-list'),
    
    path('<int:pk>/join/', GroupJoinAPIView.as_view(), name='group-join'),
    path('<int:pk>/unjoin/', GroupUnjoinAPIView.as_view(), name='group-unjoin'),
    
    path('search/<str:title>/', GroupSearchByTitleAPIView.as_view(), name='group-search'),
    path('<int:pk>/users/', GroupUsersListAPIView.as_view(), name='group-users-list'),
    
    path('<int:pk>/materials/upload/', GroupMaterialCreateAPIView.as_view(), name='group-material-list-create'),
    path('<int:pk>/materials/', GroupMaterialListAPIView.as_view(), name='group-material-list'),
    path('<int:pk>/materials/delete/<int:M_pk>/', GroupMaterialDeleteAPIView.as_view(), name='group-material-delete'),
    path('<int:pk>/materials/search/<str:title>/', SearchMaterialByTitleAPIView.as_view(), name='material-search'),
    
    path('<int:pk>/posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('<int:pk>/posts/<int:P_pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
    path('<int:pk>/list_posts/', PostListView.as_view(), name='post-liked-list'),
    path('<int:pk>/posts/<int:P_pk>/like/', LikePostAPIView.as_view(), name='like-post'),
    path('<int:pk>/posts/<int:P_pk>/unlike/', UnLikePostAPIView.as_view(), name='unlike-post'),
    
    path('<int:pk>/posts/<int:P_pk>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('<int:pk>/posts/<int:P_pk>/comments_replies/', CommentAndReplyListAPIView.as_view(), name='comment-reply-list-create' ),
    path('<int:pk>/posts/<int:P_pk>/comments/<int:C_pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
    path('<int:pk>/comments/<int:C_pk>/like/', LikeCommentAPIView.as_view(), name='like-comment'),
    path('<int:pk>/comments/<int:C_pk>/unlike/', UnLikeCommentAPIView.as_view(), name='unlike-comment'),
    
    path('<int:pk>/posts/<int:P_pk>/comments/<int:C_pk>/replies/', ReplyListCreateAPIView.as_view(), name='reply-list-create'),
    path('<int:pk>/posts/<int:P_pk>/comments/<int:C_pk>/replies/<int:R_pk>/', ReplyRetrieveUpdateDestroyAPIView.as_view(), name='reply-detail'),
    path('<int:pk>/replies/<int:R_pk>/like/', LikeReplyAPIView.as_view(), name='like-reply'),
    path('<int:pk>/replies/<int:R_pk>/unlike/', UnLikeReplyAPIView.as_view(), name='unlike-reply'),
]
