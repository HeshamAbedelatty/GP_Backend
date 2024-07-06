from django.urls import path
from .views import (
    AudioFileListCreateAPIView,
    AudioFileDetailAPIView,
    SearchAudioFiles,
    ListFavoriteAudioFiles
)

urlpatterns = [
    path('', AudioFileListCreateAPIView.as_view(), name='audiofile-list-create'),
    path('<int:pk>/', AudioFileDetailAPIView.as_view(), name='audiofile-detail'),
    path('favorites/', ListFavoriteAudioFiles.as_view(), name='audiofile-favorites'),
    path('search/<str:file_name>/', SearchAudioFiles.as_view(), name='audiofile-search'),
]