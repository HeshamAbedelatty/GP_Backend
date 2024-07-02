from rest_framework import serializers
from .models import AudioFile

class AudioFileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = AudioFile
        fields = ['id', 'user', 'file_name', 'file_path', 'duration', 'uploaded_date', 'is_favorite', 'current_position']