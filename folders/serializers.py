from rest_framework import serializers
from .models import Folder, File

class FolderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Folder
        fields = ['id', 'name','created_at', 'user']

class FileSerializer(serializers.ModelSerializer):
    folder = serializers.ReadOnlyField(source='folder.id')
    
    class Meta:
        model = File
        fields = ['id', 'media_path', 'file_type', 'folder']
