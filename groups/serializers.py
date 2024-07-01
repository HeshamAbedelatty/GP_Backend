from users.models import CustomUser as User
from rest_framework import serializers
from .models import Group, UserGroup, GroupMaterial

class GroupMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMaterial
        fields = ['title', 'media_path','uploaded_Time']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'image']

class UserGroupSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested serializer for User

    class Meta:
        model = UserGroup
        fields = ['user', 'is_owner', 'is_admin']

class GroupDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer() # Nested serializer for User
    
    class Meta:
        model = GroupMaterial
        fields = ['id', 'user', 'title', 'media_path','uploaded_Time']
        
# //////////////////////////////////////////////////////////////////////////////////////////
class UserJoinSerializer(serializers.ModelSerializer):
    group = GroupSerializer()  # Nested serializer for User

    class Meta:
        model = UserGroup
        fields = ['group', 'is_owner', 'is_admin']

# ///////////////////////////List all groups with has joined or not///////////////////////////////////////
class GroupListSerializer(serializers.ModelSerializer):
    has_joined = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ['id', 'title', 'description', 'type', 'image', 'password', 'subject', 'members', 'has_joined']

    def get_has_joined(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserGroup.objects.filter(user=request.user, group=obj).exists()
        return False