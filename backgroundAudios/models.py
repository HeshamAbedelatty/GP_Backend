from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class AudioFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='audio_files/')
    duration = models.DurationField(default=timezone.timedelta())
    current_position = models.DurationField(default=timezone.timedelta())
    uploaded_date = models.DateTimeField(default=timezone.now)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ==> {self.file_name}"

# class FavoriteAudio(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     audio_file = models.ForeignKey(AudioFile, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Favorite {self.audio_file.file_name} by {self.user.username}"

# class Playback(models.Model):
#     PLAYBACK_STATES = [
#         ('playing', 'Playing'),
#         ('paused', 'Paused'),
#         ('stopped', 'Stopped'),
#     ]
#     id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     audio_file = models.ForeignKey(AudioFile, on_delete=models.CASCADE)
#     current_position = models.DurationField()
#     state = models.CharField(max_length=10, choices=PLAYBACK_STATES)

#     def __str__(self):
#         return f"Playback of {self.audio_file.file_name} by {self.user.username}"
