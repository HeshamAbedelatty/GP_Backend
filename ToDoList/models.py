from django.db import models
from users.models import CustomUser as User
    
class ToDoList(models.Model):
    title = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class ToDoTask(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    title = models.CharField(max_length=255)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, null=True, blank=True)
    status = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title
