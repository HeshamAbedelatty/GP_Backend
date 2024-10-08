from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# {
#     "id": 5,
#     "first_name": "Mohamed",
#     "last_name": "Khalil",
#     "email": "MK@example.com",
#     "username": "Khalil",
#     "phone_number": "01234567895",
#     "faculty": "Computer Science",
#     "date_of_birth": null,
#     "image": null,
#     "rate": 0.0
# }