from users.models import CustomUser as User
from rest_framework import serializers
from .models import Post, Comment, Reply, PostLike, CommentLike, ReplyLike

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
        
# //////////////////////////////// edit post serializers ////////////////////////////////
class PostEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
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

# //////////////////////////////// Reply Serializer ////////////////////////////////
class ReplySerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    group = serializers.ReadOnlyField(source='group.title')
    comment = serializers.ReadOnlyField(source='comment.id')
    user_has_liked = serializers.SerializerMethodField()
    
    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ReplyLike.objects.filter(user=request.user, reply=obj).exists()
        return False
    
    class Meta:
        model = Reply
        fields = ['id', 'description', 'image', 'created_at', 'likes', 'user', 'group', 'comment', 'user_has_liked']

# //////////////////////////////// Comment & Reply Serializer ////////////////////////////////
class CommentReplySerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    group = serializers.ReadOnlyField(source='group.title')
    replies = ReplySerializer(many=True, read_only=True)
    user_has_liked = serializers.SerializerMethodField()
    
    def get_replies(self, obj):
        replies = obj.replies.all()
        return ReplySerializer(replies, many=True).data

    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return CommentLike.objects.filter(user=request.user, comment=obj).exists()
        return False

    class Meta:
        model = Comment
        fields = ['id', 'description', 'image', 'created_at', 'likes', 'user', 'group', 'post', 'user_has_liked', 'replies']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    group = serializers.ReadOnlyField(source='group.title')
    post = serializers.ReadOnlyField(source='post.id')
    
    class Meta:
        model = Comment
        fields = ['id', 'description', 'image', 'created_at', 'likes', 'user', 'group', 'post']

class ReplyEditSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    group = serializers.ReadOnlyField(source='group.title')
    comment = serializers.ReadOnlyField(source='comment.id')
    
    class Meta:
        model = Reply
        fields = ['id', 'description', 'image', 'created_at', 'likes', 'user', 'group', 'comment']
