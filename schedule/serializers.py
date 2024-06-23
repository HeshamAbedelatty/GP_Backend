from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'title', 'day', 'start_time', 'end_time', 'description', 'reminder_time', 'color', 'user']
        read_only_fields = ['user']
