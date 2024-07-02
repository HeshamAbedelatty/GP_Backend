from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from groups.permissions import IsAdmin, IsNotAdmin, IsJoin, IsNotOwner, IsOwner, IsUnJoin, IsMaterialOwner
from .models import Group, UserGroup, GroupMaterial
from .serializers import (GroupSerializer, UserGroupSerializer, GroupMaterialSerializer, 
                          GroupDetailSerializer, UserJoinSerializer, GroupListSerializer)
from django.contrib.auth import get_user_model

User = get_user_model()
# ///////////////////////////////List All Groups EndPoints////////////////////////////////////////
class GroupListCreateAPIView(generics.ListCreateAPIView):
    queryset = Group.objects.all().order_by('-members')
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)
    
    def perform_create(self, serializer):
        group = serializer.save()
        UserGroup.objects.create(user=self.request.user, group=group, is_admin=True, is_owner=True)

# ///////////////////////////////List All Groups EndPoints and is joined or not////////////////////////////////////////
class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.all().order_by('-members')
    serializer_class = GroupListSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
# ///////////////////////////////List Groups that i join EndPoints////////////////////////////////////////
class UserJoinedGroupsListView(generics.ListAPIView):
    serializer_class = UserJoinSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserGroup.objects.filter(user_id= self.request.user ).select_related('group')

# /////////////////////////////////Group Detail EndPoints////////////////////////////////////////
class GroupDetailAPIView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)
 
# delete group and update the pasword only by the owner   
class GroupDeleteAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()        
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) # {"message": "Joined group successfully."}, 

    
#////////////////////////////////////////////////////////////////////////////////////////////
class GroupBatchUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, IsOwner, IsAdmin) #IsOwnerOrReadOnly
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        # if not user_is_owner(self, request.user, instance):
        #     return Response({"error": "You are not the owner of this group."}, status=status.HTTP_403_FORBIDDEN)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class GroupJoinAPIView(generics.GenericAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, IsUnJoin)

    def post(self, request, *args, **kwargs):
        group_id = kwargs.get('pk')
        password = request.data.get('password', None)
        
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if group.type == 'private':
            if not password or password != group.password:
                return Response({"error": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)
        
        group.members += 1
        group.save()
        UserGroup.objects.get_or_create(user=request.user, group=group)

        return Response({"message": "Joined group successfully."}, status=status.HTTP_200_OK)


class GroupUnjoinAPIView(generics.GenericAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated, IsJoin, IsNotOwner)

    def post(self, request, *args, **kwargs):
        group_id = kwargs.get('pk')
        
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            user_group = UserGroup.objects.get(user=request.user, group=group)
            user_group.delete()
        except UserGroup.DoesNotExist:
            return Response({"error": "You are not a member of this group."}, status=status.HTTP_400_BAD_REQUEST)

        group.members -= 1
        group.save()
        
        return Response({"message": "Unjoined group successfully."}, status=status.HTTP_200_OK)

# ///////////////////////////////Search by Group Title////////////////////////////////////////
# change group serilaizer by GroupListSerializer 
class GroupSearchByTitleAPIView(generics.ListAPIView):
    serializer_class = GroupListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        title = self.request.data.get('title', None)
        if title:
            return Group.objects.filter(title__icontains=title).order_by('-members')
        # return Group.objects.all()
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

# ///////////////////////////////Group Users List////////////////////////////////////////
class GroupUsersListAPIView(generics.ListAPIView):
    serializer_class = UserGroupSerializer
    permission_classes = (IsAuthenticated, IsJoin)

    def get_queryset(self):
        group_id = self.kwargs['pk']
        return UserGroup.objects.filter(group_id=group_id).select_related('user')
    
# ///////////////////////////////Search Matrial by Title////////////////////////////////////////
class SearchMaterialByTitleAPIView(generics.ListAPIView):
    serializer_class = GroupDetailSerializer
    permission_classes = (IsAuthenticated, IsJoin)

    def get_queryset(self):
        group_id = self.kwargs['pk']
        title = self.request.data.get('title', None)
        if title:
            return GroupMaterial.objects.filter(title__icontains=title, group_id=group_id)
        # return Group.objects.all()

# ///////////////////////////////Group Material List////////////////////////////////////////
class GroupMaterialListAPIView(generics.ListAPIView):
    serializer_class = GroupDetailSerializer
    permission_classes = (IsAuthenticated, IsJoin)

    def get_queryset(self):
        group_id = self.kwargs['pk']
        return GroupMaterial.objects.filter(group_id=group_id).select_related('user')

# Create a new material for the group 
class GroupMaterialCreateAPIView(generics.CreateAPIView):
    queryset = GroupMaterial.objects.all()
    serializer_class = GroupMaterialSerializer
    permission_classes = (IsAuthenticated, IsJoin)

    def perform_create(self, serializer):
        group = Group.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, group=group)

    def get_queryset(self):
        group_id = self.kwargs['pk']
        return GroupMaterial.objects.filter(group_id=group_id)    

# Delete a material of the group
class GroupMaterialDeleteAPIView(generics.DestroyAPIView):
    queryset = GroupMaterial.objects.all()
    serializer_class = GroupMaterialSerializer
    permission_classes = (IsAuthenticated, IsJoin, IsMaterialOwner)
    
    def delete(self, request, *args, **kwargs):
        material_id = kwargs.get('M_pk')
        try:
            material = GroupMaterial.objects.get(pk=material_id)
            material.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except GroupMaterial.DoesNotExist:
            return Response({"error": "Material does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
#/////////////////////////////Posts & Comments EndPoints////////////////////////////////

# from app1.serializers import Model1Serializer
# from app1.models import Model1
# from ToDoList.permissions import IsOwnerOrReadOnly
