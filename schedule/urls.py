from django.urls import path
from .views import ScheduleCreateAPIView, ScheduleDetailAPIView

urlpatterns = [
    path('', ScheduleCreateAPIView.as_view(), name='schedule-create'),
    path('<int:pk>/', ScheduleDetailAPIView.as_view(), name='schedule-detail'),
]
