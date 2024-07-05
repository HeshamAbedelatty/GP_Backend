from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'phone_number', 'faculty', 'date_of_birth', 'image', 'rate']

    def get_rate(self, obj):
        return obj.get_rating()
   
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number', 'faculty', 'date_of_birth', 'image', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            # faculty=validated_data['faculty'],
            # date_of_birth=validated_data['date_of_birth'],
            # image=validated_data['image'],
            password=validated_data['password']
        )
        return user
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()