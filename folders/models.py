from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Folder(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')

    def __str__(self):
        return self.name

class File(models.Model):
    FILE_TYPES = [
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('other', 'Other'),
    ]

    # name = models.CharField(max_length=255, unique=True)
    media_path = models.FileField(upload_to='media/')
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return self.media_path.name
