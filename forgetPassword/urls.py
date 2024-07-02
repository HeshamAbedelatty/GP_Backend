from django.urls import path
from .views import PasswordResetView, PasswordResetConfirmView, Password_ResetView_confirm_token
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('password-reset/', csrf_exempt(PasswordResetView.as_view()), name='password-reset'),
    path('get_token/', csrf_exempt(Password_ResetView_confirm_token.as_view()), name='password-reset'),
    path('reset-password/<str:token>/', csrf_exempt(PasswordResetConfirmView.as_view()), name='password-reset-confirm'),
]

