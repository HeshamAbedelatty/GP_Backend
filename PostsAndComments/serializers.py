from users.models import CustomUser as User
from rest_framework import serializers
from .models import Post, Comment, Reply

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'image']

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    group = serializers.ReadOnlyField(source='group.title')
    
    class Meta:
        model = Post
        fields = ['id', 'description', 'image', 'created_at', 'likes', 'user', 'group']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    group = serializers.ReadOnlyField(source='group.title')
    
    class Meta:
        model = Comment
        fields = ['id', 'description', 'image', 'created_at', 'likes', 'user', 'group', 'post']

class ReplySerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    group = serializers.ReadOnlyField(source='group.title')

    class Meta:
        model = Reply
        fields = ['id', 'description', 'image', 'created_at', 'likes', 'user', 'group', 'comment']

class CommentReplySerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    group = serializers.ReadOnlyField(source='group.title')
    replies = ReplySerializer(many=True, read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'description', 'image', 'created_at', 'likes', 'user', 'group', 'post', 'replies']
