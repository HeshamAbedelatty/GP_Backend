from groups.permissions import IsJoin
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from PostsAndComments.permissions import IsCommentOwner, IsPostOwner, IsReplyOwner
from .models import Post, Comment, Reply
from .serializers import PostSerializer, CommentSerializer, ReplySerializer, CommentReplySerializer

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,IsJoin,)
    
    # def get_queryset(self):
    #     return Post.objects.all()

    def perform_create(self, serializer):
        group_id = self.kwargs.get('pk')
        serializer.save(user=self.request.user, group_id=group_id)

class PostRetrieveUpdateDestroyAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,IsJoin, IsPostOwner,)

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
# ////////////////////////////Like Post////////////////////////////////////////
# class LikePostAPIView(generics.UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (IsAuthenticated,IsJoin,)
    
#     def post (self, request, *args, **kwargs):
#         post_id = kwargs.get('P_pk')
#         if not post_id:
#             raise PermissionDenied(detail="Post ID is missing")
#         try:
#             post = Post.objects.get(id=post_id)
#             post.likes.add(request.user)
#             return Response({"message": "Post liked successfully."}, status=status.HTTP_200_OK)
#         except Post.DoesNotExist:
#             raise PermissionDenied(detail="Post does not exist")
            
#     def perform_update(self, serializer):
#         serializer.save(usr=self.request.user)
    
#     def get_queryset(self):
#         return Post.objects.filter(likes=self.request.user)
    
# ////////////////////////////Like Comment////////////////////////////////////////

    