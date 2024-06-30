from users.models import CustomUser as User
from rest_framework import serializers
from .models import Post, Comment, Reply, PostLike

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'image']

# //////////////////////////////// Post Serializer ////////////////////////////////
class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    group = serializers.ReadOnlyField(source='group.title')
    
    class Meta:
        model = Post
        fields = ['id', 'description', 'image', 'created_at', 'likes', 'user', 'group']

# ///////////////////Post List Serializer that its Liked or not////////////////////////
class PostListSerializer(serializers.ModelSerializer):
    user_has_liked = serializers.SerializerMethodField()
    user = UserSerializer()
    group = serializers.ReadOnlyField(source='group.title')

    class Meta:
        model = Post
        fields = ['id', 'description', 'image', 'created_at', 'likes', 'user_has_liked', 'group', 'user']

    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(user=request.user, post=obj).exists()
        return False


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
    user_has_liked = serializers.SerializerMethodField()
    
    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(user=request.user, post=obj).exists()
        return False
    class Meta:
        model = Comment
        fields = ['id', 'description', 'image', 'created_at', 'likes', 'group', 'post', 'user', 'replies']


# //////////////////////////////// PostLike Serializer ////////////////////////////////
# class PostSerializer(serializers.ModelSerializer):
#     user = UserSerializer() 
#     group = serializers.ReadOnlyField(source='group.title')
    
#     class Meta:
#         model = Post
#         fields = ['id', 'description', 'image', 'created_at', 'likes', 'user', 'group']