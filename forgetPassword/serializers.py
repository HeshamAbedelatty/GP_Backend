from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate_token(self, value):
        if not User.objects.filter(profile__reset_password_token=value).exists():
            raise serializers.ValidationError("Invalid or expired token.")
        return value
