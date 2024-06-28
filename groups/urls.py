
from django.urls import path
from . import views
from .views import GroupSearchByTitleAPIView, GroupJoinAPIView, GroupDeleteAPIView, GroupUsersListAPIView
from .views import GroupUnjoinAPIView, GroupListCreateAPIView, GroupDetailAPIView, GroupBatchUpdateAPIView
from .views import GroupMaterialCreateAPIView, GroupMaterialListAPIView, GroupMaterialDeleteAPIView

urlpatterns = [
    path('', GroupListCreateAPIView.as_view(), name='group-list-create'),
    path('<int:pk>/', GroupDetailAPIView.as_view(), name='group-detail'),
    path('patch_update/<int:pk>/', GroupBatchUpdateAPIView.as_view(), name='group-batch-update'),
    path('delete_patch/<int:pk>/', GroupDeleteAPIView.as_view(), name='group-delete'),
    path('<int:pk>/join/', GroupJoinAPIView.as_view(), name='group-join'),
    path('<int:pk>/unjoin/', GroupUnjoinAPIView.as_view(), name='group-unjoin'),
    path('search/', GroupSearchByTitleAPIView.as_view(), name='group-search'),
    path('<int:pk>/users/', GroupUsersListAPIView.as_view(), name='group-users-list'),
    path('<int:pk>/materials/upload/', GroupMaterialCreateAPIView.as_view(), name='group-material-list-create'),
    path('<int:pk>/materials/', GroupMaterialListAPIView.as_view(), name='group-material-list'),
    path('<int:pk>/materials/delete/<int:M_pk>/', GroupMaterialDeleteAPIView.as_view(), name='group-material-delete'),
]
