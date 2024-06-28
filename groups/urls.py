
from django.urls import path
from . import views
from .views import GroupSearchByTitleAPIView, GroupJoinAPIView, GroupDeleteAPIView,GroupUnjoinAPIView, GroupListCreateAPIView, GroupDetailAPIView, GroupBatchUpdateAPIView

urlpatterns = [
    path('', GroupListCreateAPIView.as_view(), name='group-list-create'),
    path('<int:pk>/', GroupDetailAPIView.as_view(), name='group-detail'),
    path('patch_update/<int:pk>/', GroupBatchUpdateAPIView.as_view(), name='group-batch-update'),
    path('delete_patch/<int:pk>/', GroupDeleteAPIView.as_view(), name='group-delete'),
    path('<int:pk>/join/', GroupJoinAPIView.as_view(), name='group-join'),
    path('<int:pk>/unjoin/', GroupUnjoinAPIView.as_view(), name='group-unjoin'),
    path('search/', views.GroupSearchByTitleAPIView.as_view(), name='group-search')
]
