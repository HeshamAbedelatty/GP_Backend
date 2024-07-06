from django.urls import path
from .views import RecommendationSystem

urlpatterns = [
    path('', RecommendationSystem.as_view(), name='recommend_response'),
]