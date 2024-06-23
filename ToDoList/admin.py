from django.contrib import admin
from .models import ToDoList, ToDoTask
# Register your models here.

admin.site.register(ToDoList)
admin.site.register(ToDoTask)
