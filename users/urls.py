from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, LogoutView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),

]
