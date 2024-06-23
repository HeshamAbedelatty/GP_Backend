from django.urls import path
from .views import ToDoTaskView, ToDoTaskDetailView, ToDoListView, ToDoListDetailView

urlpatterns = [
    path('', ToDoListView.as_view(), name='todolist-list'),
    path('<int:pk>/', ToDoListDetailView.as_view(), name='todolist-detail'),
    path('<int:todolist_pk>/tasks/', ToDoTaskView.as_view(), name='todotask-list'),
    path('<int:todolist_pk>/tasks/<int:pk>/', ToDoTaskDetailView.as_view(), name='todotask-detail'),
]
