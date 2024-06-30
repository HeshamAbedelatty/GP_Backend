from groups.permissions import IsJoin
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from PostsAndComments.permissions import (
    IsCommentOwner, IsPostOwner, IsReplyOwner, IsPostInGroup)
from .models import Comment, Post, PostLike, Reply
from .serializers import (PostSerializer, CommentSerializer, ReplySerializer, 
                          CommentReplySerializer, PostListSerializer)

# ////////////////////////////Create Post////////////////////////////////////////
class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,IsJoin,)
    
    def perform_create(self, serializer):
        group_id = self.kwargs.get('pk')
        serializer.save(user=self.request.user, group_id=group_id)

# ////////////////////////////List Post with if its liked or not////////////////////////////////////////
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated, IsJoin]

    def get_queryset(self):
        group_id = self.kwargs.get('pk')
        return Post.objects.filter(group_id=group_id).select_related('user').order_by('-created_at')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class PostRetrieveUpdateDestroyAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,IsJoin, IsPostOwner,)

# ////////////////////////////Like Post////////////////////////////////////////
class LikePostAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,IsJoin, IsPostInGroup,)
    
    def post (self, request, *args, **kwargs):
        post_id = kwargs.get('P_pk')
        if not post_id:
            raise PermissionDenied(detail="Post ID is missing")
        try:
            if PostLike.objects.filter(user=request.user, post_id=post_id).exists():
                raise PermissionDenied(detail="Post is already liked by the user")
            post = Post.objects.get(id=post_id)
            post.likes += 1
            post.save()
            PostLike.objects.create(user=request.user, post=post)
            return Response({"message": "Post liked successfully."}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise PermissionDenied(detail="Post does not exist")
            
    def perform_update(self, serializer):
        serializer.save(usr=self.request.user)
    
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

# ////////////////////////////UnLike Post////////////////////////////////////////
class UnLikePostAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,IsJoin, IsPostInGroup,)
    
    def post (self, request, *args, **kwargs):
        post_id = kwargs.get('P_pk')
        if not post_id:
            raise PermissionDenied(detail="Post ID is missing")
        try:
            if not PostLike.objects.filter(user=request.user, post_id=post_id).exists():
                raise PermissionDenied(detail="Post is not liked by the user")
            post = Post.objects.get(id=post_id)
            post.likes -= 1
            post.save()
            PostLike.objects.filter(user=request.user, post=post).delete()
            return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise PermissionDenied(detail="Post does not exist")
            
    def perform_update(self, serializer):
        serializer.save(usr=self.request.user)
    
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


# ////////////////////////////Create Comment////////////////////////////////////////
class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,IsJoin,)
    def perform_create(self, serializer):
        group_id = self.kwargs.get('pk')
        post_id = self.kwargs.get('P_pk')
        serializer.save(user=self.request.user, group_id=group_id, post_id=post_id)

# ////////////////////////////List Comment and Replys////////////////////////////////////////


# ////////////////////////////Edit in Comment////////////////////////////////////////
class CommentRetrieveUpdateDestroyAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,IsJoin, IsCommentOwner,)

class ReplyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = (IsAuthenticated,IsJoin,)

class ReplyRetrieveUpdateDestroyAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = (IsAuthenticated,IsJoin, IsReplyOwner,)
    

class CommentReplyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentReplySerializer
    permission_classes = (IsAuthenticated,IsJoin,)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializer
        return CommentSerializer

    
# ////////////////////////////Like Comment////////////////////////////////////////

    