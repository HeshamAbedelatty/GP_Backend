from rest_framework import generics, permissions
from .models import Folder, File
from .serializers import FolderSerializer, FileSerializer

class FolderListCreateView(generics.ListCreateAPIView):
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FolderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FolderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)

class FileListCreateView(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        folder_id = self.kwargs['folder_id']
        return File.objects.filter(folder__id=folder_id, folder__user=self.request.user)

    def perform_create(self, serializer):
        folder = Folder.objects.get(pk=self.kwargs['folder_id'], user=self.request.user)
        serializer.save(folder=folder)

class FileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        folder_id = self.kwargs['folder_id']
        return File.objects.filter(folder__id=folder_id, folder__user=self.request.user)
