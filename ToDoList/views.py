from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import ToDoTask, ToDoList
from .serializers import ToDoTaskSerializer, ToDoListSerializer

class ToDoListView(ListCreateAPIView):
    queryset = ToDoList.objects.all()
    serializer_class = ToDoListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)

class ToDoListDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ToDoList.objects.all()
    serializer_class = ToDoListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Schedule deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ToDoTaskView(ListCreateAPIView):
    queryset = ToDoTask.objects.all()
    serializer_class = ToDoTaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        todo_list = ToDoList.objects.get(pk=self.kwargs['todolist_pk'])
        serializer.save(todo_list=todo_list)

    # def get_queryset(self):
    #     return ToDoTask.objects.filter(todo_list__user=self.request.user)
    def get_queryset(self):
        return ToDoTask.objects.filter(todo_list__user=self.request.user, todo_list_id=self.kwargs['todolist_pk'])


class ToDoTaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ToDoTask.objects.all()
    serializer_class = ToDoTaskSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return ToDoTask.objects.filter(todo_list__user=self.request.user)
    def get_queryset(self):
        return ToDoTask.objects.filter(todo_list__user=self.request.user, todo_list_id=self.kwargs['todolist_pk'])
    
    # def patch(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     if 'status' in request.data:
    #         instance.status = request.data['status']
    #         instance.save()
    #         return Response({"message": "Status updated successfully"}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({"error": "Missing 'status' field in request data"}, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Schedule deleted successfully"}, status=status.HTTP_204_NO_CONTENT)