from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from folders.models import Folder
from forgetPassword.models import Profile
from backgroundAudios.models import AudioFile
from datetime import timedelta

@receiver(post_save, sender=CustomUser)
def create_favorites_folder(sender, instance, created, **kwargs):
    if created:
        Folder.objects.create(name="Favorites", user=instance)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(post_save, sender=CustomUser)
def create_default_audio_files(sender, instance, created, **kwargs):
    if created:
        default_audio_files = [
            {
                "file_name": "Light Rain",
                "file_path": "sounds/light-rain-109591.mp3",
                "duration": "0:01:44"  # Example duration
            },
            {
                "file_name": "Ocean Waves",
                "file_path": "/sounds/ocean-sea-soft-waves-121349.mp3",
                "duration": "0:03:00"
            },
            {
                "file_name": "Smooth Cold Wind",
                "file_path": "/sounds/smooth-cold-wind-looped-135538.mp3",
                "duration": "0:03:00"
            }
        ]
        
        for audio_file in default_audio_files:
            AudioFile.objects.create(
                user=instance,
                file_name=audio_file["file_name"],
                file_path=audio_file["file_path"],
                duration=parse_duration(audio_file["duration"])
            )

def parse_duration(duration_str):
    """Parse a duration string in the format 'HH:MM:SS' into a timedelta object."""
    try:
        hours, minutes, seconds = map(int, duration_str.split(':'))
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    except ValueError:
        raise ValueError("Duration format should be 'HH:MM:SS'")