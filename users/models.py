from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    faculty = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.username
