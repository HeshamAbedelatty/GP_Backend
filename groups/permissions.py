from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import UserGroup

class IsOwner(BasePermission):
    """
    Custom permission to check if the user is the owner of the group.
    """

    def has_permission(self, request, view):
        group_id = view.kwargs.get('pk')
        if not group_id:
            raise PermissionDenied(detail="Group ID is missing")

        try:
            user_group = UserGroup.objects.get(user=request.user, group_id=group_id)
            if user_group.is_owner:
                return True
            else:
                raise PermissionDenied(detail="You are not the owner of this group")
        except UserGroup.DoesNotExist:
            raise PermissionDenied(detail="This group is Deleted or You are not a member of this group")

class IsNotOwner(BasePermission):
    """
    Custom permission to check if the user is not the owner of the group.
    """

    def has_permission(self, request, view):
        group_id = view.kwargs.get('pk')
        if not group_id:
            raise PermissionDenied(detail="Group ID is missing")

        try:
            user_group = UserGroup.objects.get(user=request.user, group_id=group_id)
            if not user_group.is_owner:
                return True
            else:
                raise PermissionDenied(detail="You are the owner of this group")
        except UserGroup.DoesNotExist:
            raise PermissionDenied(detail="This group is Deleted or You are not a member of this group")

class IsAdmin(BasePermission):
    """
    Custom permission to check if the user is the admin of the group.
    """

    def has_permission(self, request, view):
        group_id = view.kwargs.get('pk')
        if not group_id:
            raise PermissionDenied(detail="Group ID is missing")

        try:
            user_group = UserGroup.objects.get(user=request.user, group_id=group_id)
            if user_group.is_admin:
                return True
            else:
                raise PermissionDenied(detail="You are not the admin of this group")
        except UserGroup.DoesNotExist:
            raise PermissionDenied(detail="This group is Deleted or You are not a member of this group")

class IsNotAdmin(BasePermission):
    """
    Custom permission to check if the user is not the admin of the group.
    """

    def has_permission(self, request, view):
        group_id = view.kwargs.get('pk')
        if not group_id:
            raise PermissionDenied(detail="Group ID is missing")

        try:
            user_group = UserGroup.objects.get(user=request.user, group_id=group_id)
            if not user_group.is_admin:
                return True
            else:
                raise PermissionDenied(detail="You are the admin of this group")
        except UserGroup.DoesNotExist:
            raise PermissionDenied(detail="This group is Deleted or You are not a member of this group")

class IsJoin (BasePermission):
    """
    Custom permission to check if the user is Joined to the group.
    """

    def has_permission(self, request, view):
        group_id = view.kwargs.get('pk')
        if not group_id:
            raise PermissionDenied(detail="Group ID is missing")
        
        try:
            return UserGroup.objects.filter(user=request.user, group_id=group_id).exists()
        except UserGroup.DoesNotExist:
            raise PermissionDenied(detail="This group is Deleted or You are not a member of this group")
        
class IsUnJoin (BasePermission):
    """
    Custom permission to check if the user is njoined of the group.
    """

    def has_permission(self, request, view):
        group_id = view.kwargs.get('pk')
        if not group_id:
            raise PermissionDenied(detail="Group ID is missing")
        try:
            if not UserGroup.objects.filter(user=request.user, group_id=group_id).exists():
                return True  
        except UserGroup.DoesNotExist:
            raise PermissionDenied(detail="You are already member of this group")