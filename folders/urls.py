from django.urls import path
from .views import FolderListCreateView, FolderRetrieveUpdateDestroyView, FileListCreateView, FileRetrieveUpdateDestroyView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', FolderListCreateView.as_view(), name='folder-list-create'),
    path('<int:pk>/', FolderRetrieveUpdateDestroyView.as_view(), name='folder-retrieve-update-destroy'),
    path('<int:folder_id>/files/', FileListCreateView.as_view(), name='file-list-create'),
    path('<int:folder_id>/files/<int:pk>/', FileRetrieveUpdateDestroyView.as_view(), name='file-retrieve-update-destroy'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
