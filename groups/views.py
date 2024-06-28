from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from groups.permissions import IsAdmin, IsNotAdmin, IsJoin, IsNotOwner, IsOwner, IsUnJoin
from .models import Group, UserGroup
from .serializers import GroupSerializer

class GroupListCreateAPIView(generics.ListCreateAPIView):
    queryset = Group.objects.all().order_by('-members')
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)
    
    def perform_create(self, serializer):
        group = serializer.save()
        UserGroup.objects.create(user=self.request.user, group=group, is_admin=True, is_owner=True)
        
        
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
    
    
# def user_is_owner(self, user, group):
#         return UserGroup.objects.filter(user=user, group=group, is_owner=True).exists()
        

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

class GroupSearchByTitleAPIView(generics.ListAPIView):
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        title = self.request.data.get('title', None)
        if title:
            return Group.objects.filter(title__icontains=title)
        # return Group.objects.all()