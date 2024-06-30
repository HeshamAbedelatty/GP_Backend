from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Schedule(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    title = models.CharField(max_length=255)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True)
    # reminder_time = models.DateTimeField(null=True, blank=True)
    reminder_time = models.IntegerField(default=0)
    color = models.CharField(max_length=50, null=True, blank=True, default='#007bff')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')

    def __str__(self):
        return self.title
