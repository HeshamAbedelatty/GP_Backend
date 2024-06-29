from groups.permissions import IsJoin
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
import rest_framework.permissions
from PostsAndComments.permissions import IsCommentOwner, IsReplyOwner
from .models import Post, Comment, Reply
from .serializers import PostSerializer, CommentSerializer, ReplySerializer

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,IsJoin,)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostRetrieveUpdateDestroyAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,IsJoin,)
    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
    
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
