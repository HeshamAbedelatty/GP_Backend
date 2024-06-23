from rest_framework import serializers
from .models import ToDoTask, ToDoList

class ToDoTaskSerializer(serializers.ModelSerializer):
    # todo_list = serializers.ReadOnlyField(source='todo_list.name')
    todo_list = serializers.PrimaryKeyRelatedField(queryset=ToDoList.objects.all())
    
    class Meta:
        model = ToDoTask
        fields = ['id', 'title', 'priority', 'status','due_date', 'todo_list']

class ToDoListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ToDoList
        fields = ['id', 'title', 'user']
        