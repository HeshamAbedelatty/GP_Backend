
from django.urls import path
from .views import (
    SearchMaterialByTitleAPIView,
    GroupSearchByTitleAPIView, GroupJoinAPIView, GroupDeleteAPIView, GroupUsersListAPIView,
    GroupUnjoinAPIView, GroupListCreateAPIView, GroupDetailAPIView, GroupBatchUpdateAPIView,
    GroupMaterialCreateAPIView, GroupMaterialListAPIView, GroupMaterialDeleteAPIView,
    UserJoinedGroupsListView,
)

from PostsAndComments.views import (
    PostListCreateAPIView,
    PostRetrieveUpdateDestroyAPIView,
    CommentListCreateAPIView,
    CommentRetrieveUpdateDestroyAPIView,
    ReplyListCreateAPIView,
    ReplyRetrieveUpdateDestroyAPIView,
    CommentReplyListCreateAPIView,
)

urlpatterns = [
    path('', GroupListCreateAPIView.as_view(), name='group-list-create'),
    path('<int:pk>/', GroupDetailAPIView.as_view(), name='group-detail'),
    path('patch_update/<int:pk>/', GroupBatchUpdateAPIView.as_view(), name='group-batch-update'),
    path('delete_patch/<int:pk>/', GroupDeleteAPIView.as_view(), name='group-delete'),
    path('user_joined_groups/', UserJoinedGroupsListView.as_view(), name='user-joined-groups'),
    
    path('<int:pk>/join/', GroupJoinAPIView.as_view(), name='group-join'),
    path('<int:pk>/unjoin/', GroupUnjoinAPIView.as_view(), name='group-unjoin'),
    
    path('search/', GroupSearchByTitleAPIView.as_view(), name='group-search'),
    path('<int:pk>/users/', GroupUsersListAPIView.as_view(), name='group-users-list'),
    
    path('<int:pk>/materials/upload/', GroupMaterialCreateAPIView.as_view(), name='group-material-list-create'),
    path('<int:pk>/materials/', GroupMaterialListAPIView.as_view(), name='group-material-list'),
    path('<int:pk>/materials/delete/<int:M_pk>/', GroupMaterialDeleteAPIView.as_view(), name='group-material-delete'),
    path('<int:pk>/materials/search/', SearchMaterialByTitleAPIView.as_view(), name='material-search'),
    
    path('<int:pk>/posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('<int:pk>/posts/<int:P_pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),

    path('<int:pk>/posts/<int:P_pk>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('<int:pk>/posts/<int:P_pk>/comments_replies/', CommentReplyListCreateAPIView.as_view(), name='comment-reply-list-create' ),
    path('<int:pk>/posts/<int:P_pk>/comments/<int:C_pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),

    path('<int:pk>/posts/<int:P_pk>/comments/<int:C_pk>/replies/', ReplyListCreateAPIView.as_view(), name='reply-list-create'),
    path('<int:pk>/posts/<int:P_pk>/comments/<int:C_pk>/replies/<int:R_pk>/', ReplyRetrieveUpdateDestroyAPIView.as_view(), name='reply-detail'),

]
