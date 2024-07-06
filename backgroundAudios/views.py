from rest_framework import generics, permissions
from .models import AudioFile
from .serializers import AudioFileSerializer

# /////////////////////////////////AudioFile EndPoints////////////////////////////////////////
class AudioFileListCreateAPIView(generics.ListCreateAPIView):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AudioFileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class ListFavoriteAudioFiles(generics.ListAPIView):
    serializer_class = AudioFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AudioFile.objects.filter(user=self.request.user, is_favorite=True)

class SearchAudioFiles(generics.ListAPIView):
    serializer_class = AudioFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        file_name = self.kwargs.get('file_name', None)
        if file_name:
            return AudioFile.objects.filter(user=self.request.user, file_name__icontains=file_name)
        return AudioFile.objects.all()