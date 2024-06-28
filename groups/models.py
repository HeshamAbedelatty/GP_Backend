from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Group(models.Model):
    GROUP_TYPES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    type = models.CharField(max_length=10, choices=GROUP_TYPES)
    image = models.ImageField(upload_to='groupsPhotoes/', null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)  # Only for private groups
    subject = models.CharField(max_length=255, null=True, blank=True)
    members = models.IntegerField(default=1)
    def save(self, *args, **kwargs):
        if self.type == 'public':
            self.password = None
        elif self.type == 'private' and self.password is None:
            raise ValidationError('Password is required')
        super(Group, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title

class GroupMaterial(models.Model):
    title = models.CharField(max_length=255)
    media_path = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='materials')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.group.title} - {self.user.username}"

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.group.title}"
