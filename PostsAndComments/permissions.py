from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from forgetPassword.views import logger
from .models import Post, Comment, Reply
from groups.models import UserGroup

class IsPostOwner(BasePermission):
    """
    Custom permission to check if the user is the owner of the post.
    """

    def has_permission(self, request, view):
        post_id = view.kwargs.get('P_pk')
        group_id = view.kwargs.get('pk')
        if not post_id:
            raise PermissionDenied(detail="Post ID is missing")

        try:
            post = Post.objects.get(user=request.user, id=post_id)
            logger.info(f"Post: {post}")
            if post.user == request.user:
                return True
            elif UserGroup.objects.filter(user=request.user, group=post.group, is_admin=True).exists():
                return True
            else:
                raise PermissionDenied(detail="You are not the owner of this post or admin of the group")
        except Post.DoesNotExist:
            raise PermissionDenied(detail="You are not the owner of this post")

class IsCommentOwner(BasePermission):
    """
    Custom permission to check if the user is the owner of the comment.
    """

    def has_permission(self, request, view):
        comment_id = view.kwargs.get('C_pk')
        if not comment_id:
            raise PermissionDenied(detail="Comment ID is missing")

        try:
            comment = Comment.objects.get(user=request.user, id=comment_id)
            if comment.user == request.user:
                return True
            elif UserGroup.objects.filter(user=request.user, group=comment.group, is_admin=True).exists():
                return True
        except Comment.DoesNotExist:
            raise PermissionDenied(detail="You are not the owner of this comment or admin of the group")

class IsReplyOwner(BasePermission):
    """
    Custom permission to check if the user is the owner of the reply.
    """

    def has_permission(self, request, view):
        reply_id = view.kwargs.get('R_pk')
        if not reply_id:
            raise PermissionDenied(detail="Reply ID is missing")

        try:
            reply = Reply.objects.get(user=request.user, id=reply_id)
            return True
        except Reply.DoesNotExist:
            raise PermissionDenied(detail="You are not the owner of this reply")
        
class IsPostInGroup(BasePermission):
    """
    Custom permission to check if the post is in the group.
    """

    def has_permission(self, request, view):
        post_id = view.kwargs.get('P_pk')
        group_id = view.kwargs.get('pk')
        if not post_id:
            raise PermissionDenied(detail="Post ID is missing")

        try:
            post = Post.objects.get(id=post_id)
            if post.group.id == group_id:
                return True
            else:
                raise PermissionDenied(detail="Post is not in this group")
        except Post.DoesNotExist:
            raise PermissionDenied(detail="you are not a member of this group")