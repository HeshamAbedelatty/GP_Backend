import django.contrib.auth.tokens
from groups.permissions import IsJoin
from forgetPassword.views import logger
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from PostsAndComments.permissions import (
    IsCommentOwner, IsPostOwner, IsReplyOwner, IsPostInGroup)
from .models import Comment, Post, PostLike, Reply, CommentLike, ReplyLike
from .serializers import (PostSerializer, CommentSerializer, ReplySerializer, ReplyEditSerializer,
                          CommentReplySerializer, PostListSerializer, CommentEditSerializer)

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

# ////////////////////////////Edit Post////////////////////////////////////////
class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated,IsJoin, IsPostOwner,)
    
    
    def retrieve(self, request, *args, **kwargs):
        post_id = kwargs.get('P_pk')
        group_id = kwargs.get('pk')
        if not post_id:
            raise PermissionDenied(detail="Post ID is missing")
        try:
            post = Post.objects.get(id=post_id)
            if post.group.id != group_id:
                raise PermissionDenied(detail="Post does not belong to this group")
            serializer = PostListSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Post.DoesNotExist:
            raise PermissionDenied(detail="Post does not exist")
    
    def patch (self, request, *args, **kwargs):
        post_id = kwargs.get('P_pk')
        group_id = kwargs.get('pk')
        if not post_id:
            raise PermissionDenied(detail="Post ID is missing")
        try:
            post = Post.objects.get(id=post_id)
            if post.group.id != group_id:
                raise PermissionDenied(detail="Post does not belong to this group")
            serializer = PostListSerializer(post, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            raise PermissionDenied(detail="Post does not exist")
    
    def delete(self, request, *args, **kwargs):
        post_id = kwargs.get('P_pk')
        group_id = kwargs.get('pk')
        if not post_id:
            raise PermissionDenied(detail="Post ID is missing")
        try:
            post = Post.objects.get(id=post_id)
            if post.group.id != group_id:
                raise PermissionDenied(detail="Post does not belong to this group")
            post.delete()
            return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            raise PermissionDenied(detail="Post does not exist")
    
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
class CommentAndReplyListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentReplySerializer
    permission_classes = (IsAuthenticated,IsJoin,)
    
    def get_queryset(self):
        post_id = self.kwargs.get('P_pk')
        return Comment.objects.filter(post_id=post_id).select_related('user').order_by('created_at')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

# ////////////////////////////Edit in Comment////////////////////////////////////////
class CommentRetrieveUpdateDestroyAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentReplySerializer
    permission_classes = (IsAuthenticated,IsJoin, IsCommentOwner,)
        
    def retrieve(self, request, *args, **kwargs):
        comment_id = kwargs.get('C_pk')
        post_id = kwargs.get('P_pk')
        if not comment_id:
            raise PermissionDenied(detail="Comment ID is missing")
        try:
            comment = Comment.objects.get(id=comment_id)
            if comment.post.id != post_id:
                raise PermissionDenied(detail="Comment does not belong to this post")
            serializer = CommentReplySerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Comment.DoesNotExist:
            raise PermissionDenied(detail="Comment does not exist")
    
    def patch (self, request, *args, **kwargs):
        comment_id = kwargs.get('C_pk')
        post_id = kwargs.get('P_pk')
        if not comment_id:
            raise PermissionDenied(detail="Comment ID is missing")
        try:
            comment = Comment.objects.get(id=comment_id)
            if comment.post.id != post_id:
                raise PermissionDenied(detail="Comment does not belong to this post")
            serializer = CommentReplySerializer(comment, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            raise PermissionDenied(detail="Comment does not exist")
    
    def delete(self, request, *args, **kwargs):
        comment_id = kwargs.get('C_pk')
        post_id = kwargs.get('P_pk')
        if not comment_id:
            raise PermissionDenied(detail="Comment ID is missing")
        try:
            comment = Comment.objects.get(id=comment_id)
            if comment.post.id != post_id:
                raise PermissionDenied(detail="Comment does not belong to this post")
            comment.delete()
            return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            raise PermissionDenied(detail="Comment does not exist")
        
# ////////////////////////////Like Comment////////////////////////////////////////
class LikeCommentAPIView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,IsJoin,)
    
    def post (self, request, *args, **kwargs):
        comment_id = kwargs.get('C_pk')
        if not comment_id:
            raise PermissionDenied(detail="Comment ID is missing")
        try:
            if CommentLike.objects.filter(user=request.user, comment_id=comment_id).exists():
                raise PermissionDenied(detail="Comment is already liked by the user")
            comment = Comment.objects.get(id=comment_id)
            comment.likes += 1
            comment.save()
            CommentLike.objects.create(user=request.user, comment=comment)
            return Response({"message": "Comment liked successfully."}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            raise PermissionDenied(detail="Comment does not exist")
            
    def perform_update(self, serializer):
        serializer.save(usr=self.request.user)
    
    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

# ////////////////////////////UnLike Comment////////////////////////////////////////
class UnLikeCommentAPIView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,IsJoin,)
    
    def post (self, request, *args, **kwargs):
        comment_id = kwargs.get('C_pk')
        if not comment_id:
            raise PermissionDenied(detail="Comment ID is missing")
        try:
            if not CommentLike.objects.filter(user=request.user, comment_id=comment_id).exists():
                raise PermissionDenied(detail="Comment is not liked by the user")
            comment = Comment.objects.get(id=comment_id)
            comment.likes -= 1
            comment.save()
            CommentLike.objects.filter(user=request.user, comment=comment).delete()
            return Response({"message": "Comment unliked successfully."}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            raise PermissionDenied(detail="Comment does not exist")
            
    def perform_update(self, serializer):
        serializer.save(usr=self.request.user)
    
    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

# ////////////////////////////Create Reply////////////////////////////////////////
class ReplyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplyEditSerializer
    permission_classes = (IsAuthenticated,IsJoin,)

    def perform_create(self, serializer):
        group_id = self.kwargs.get('pk')
        comment_id = self.kwargs.get('C_pk')
        serializer.save(user=self.request.user, group_id=group_id, comment_id=comment_id)
    
# ////////////////////////////Edit Reply////////////////////////////////////////
class ReplyRetrieveUpdateDestroyAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = (IsAuthenticated,IsJoin, IsReplyOwner,)
    
    def retrieve(self, request, *args, **kwargs):
        reply_id = kwargs.get('R_pk')
        comment_id = kwargs.get('C_pk')
        post_id = kwargs.get('P_pk')
        if not reply_id:
            raise PermissionDenied(detail="Reply ID is missing")
        try:
            reply = Reply.objects.get(id=reply_id)
            if reply.comment.id != comment_id:
                raise PermissionDenied(detail="Reply does not belong to this comment")
            serializer = ReplySerializer(reply, context={'request': request})
            return Response(serializer.data)
        except Reply.DoesNotExist:
            raise PermissionDenied(detail="Reply does not exist")
    
    def patch (self, request, *args, **kwargs):
        reply_id = kwargs.get('R_pk')
        comment_id = kwargs.get('C_pk')
        post_id = kwargs.get('P_pk')
        if not reply_id:
            raise PermissionDenied(detail="Reply ID is missing")
        try:
            reply = Reply.objects.get(id=reply_id)
            if reply.comment.id != comment_id:
                raise PermissionDenied(detail="Reply does not belong to this comment")
            serializer = ReplySerializer(reply, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Reply.DoesNotExist:
            raise PermissionDenied(detail="Reply does not exist")
        
    def delete(self, request, *args, **kwargs):
        reply_id = kwargs.get('R_pk')
        comment_id = kwargs.get('C_pk')
        post_id = kwargs.get('P_pk')
        if not reply_id:
            raise PermissionDenied(detail="Reply ID is missing")
        try:
            reply = Reply.objects.get(id=reply_id)
            if reply.comment.id != comment_id:
                raise PermissionDenied(detail="Reply does not belong to this comment")
            reply.delete()
            return Response({"message": "Reply deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Reply.DoesNotExist:
            raise PermissionDenied(detail="Reply does not exist")

# ////////////////////////////Like Reply////////////////////////////////////////
class LikeReplyAPIView(generics.UpdateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = (IsAuthenticated,IsJoin,)
    
    def post (self, request, *args, **kwargs):
        reply_id = kwargs.get('R_pk')
        if not reply_id:
            raise PermissionDenied(detail="Reply ID is missing")
        try:
            if ReplyLike.objects.filter(user=request.user, reply_id=reply_id).exists():
                raise PermissionDenied(detail="Reply is already liked by the user")
            reply = Reply.objects.get(id=reply_id)
            reply.likes += 1
            reply.save()
            ReplyLike.objects.create(user=request.user, reply=reply)
            return Response({"message": "Reply liked successfully."}, status=status.HTTP_200_OK)
        except Reply.DoesNotExist:
            raise PermissionDenied(detail="Reply does not exist")
            
    def perform_update(self, serializer):
        serializer.save(usr=self.request.user)
    
    def get_queryset(self):
        return Reply.objects.filter(user=self.request.user)

# ////////////////////////////UnLike Reply////////////////////////////////////////
class UnLikeReplyAPIView(generics.UpdateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = (IsAuthenticated,IsJoin,)
    
    def post (self, request, *args, **kwargs):
        reply_id = kwargs.get('R_pk')
        if not reply_id:
            raise PermissionDenied(detail="Reply ID is missing")
        try:
            if not ReplyLike.objects.filter(user=request.user, reply_id=reply_id).exists():
                raise PermissionDenied(detail="Reply is not liked by the user")
            reply = Reply.objects.get(id=reply_id)
            reply.likes -= 1
            reply.save()
            ReplyLike.objects.filter(user=request.user, reply=reply).delete()
            return Response({"message": "Reply unliked successfully."}, status=status.HTTP_200_OK)
        except Reply.DoesNotExist:
            raise PermissionDenied(detail="Reply does not exist")
            
    def perform_update(self, serializer):
        serializer.save(usr=self.request.user)
    
    def get_queryset(self):
        return Reply.objects.filter(user=self.request.user)