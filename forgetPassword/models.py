
from django.db import models
# from users.models import CustomUser as User
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username




# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
