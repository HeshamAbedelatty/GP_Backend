from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from folders.models import Folder

@receiver(post_save, sender=CustomUser)
def create_favorites_folder(sender, instance, created, **kwargs):
    if created:
        Folder.objects.create(name="Favorites", user=instance)
