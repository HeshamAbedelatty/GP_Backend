from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import PasswordResetSerializer, PasswordResetConfirmSerializer
from django.core.mail import send_mail
from users.models import CustomUser as User
from .models import Profile
# from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth.forms import SetPasswordForm
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class PasswordResetView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     @csrf_exempt
#     def post(self, request):
#         serializer = PasswordResetSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             user = User.objects.get(email=email)
#             token = get_random_string(20)
#             user.profile.reset_password_token = token  # Assuming you have a Profile model linked to User with reset_password_token field
#             user.profile.save()
#
#             reset_url = f"{request.scheme}://{request.get_host()}/reset-password/{token}/"
#
#             send_mail(
#                 'Password Reset Request',
#                 f'Click the link to reset your password: {reset_url}',
#                 'your-email@example.com',
#                 [email],
#                 fail_silently=False,
#             )
#
#             return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import PasswordResetSerializer
from django.core.mail import send_mail
from users.models import CustomUser as User
from django.utils.crypto import get_random_string
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetView(APIView):


    @csrf_exempt
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                logger.info("kkkkkk")
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

            token = get_random_string(20)
            user_confirm=Profile.objects.get(user=user)
            user_confirm.reset_password_token = token  # Assuming you have a Profile model linked to User with reset_password_token field
            user_confirm.save()

            reset_url = f"{request.scheme}://{request.get_host()}/reset/reset-password/{token}/"

            try:


                email_user = 'mohamed9999ah@gmail.com'
                email_password = 'mdhmvhapwmpiaued'
                email_send = email #'modebeboo.20002@gmail.com'

                subject = 'Reset Passwrod Email'

                msg = MIMEMultipart()
                msg['From'] = email_user
                msg['To'] = email_send
                msg['Subject'] = subject

                body = reset_url
                msg.attach(MIMEText(body, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email_user, email_password)
                text = msg.as_string()
                server.sendmail(email_user, email_send, text)
                server.quit()
                return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error sending email: {e}")
                return Response({"error": "Error sending email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmView(APIView):

    @csrf_exempt
    def get(self, request, token):
        try:
            profile = Profile.objects.get(reset_password_token=token)
            user = profile.user
        except Profile.DoesNotExist:
            user = None

        if user is not None and profile.reset_password_token == token:
            form = SetPasswordForm(user)
            return render(request, 'reset_password.html', {'form': form,'token':token})
        else:
            return HttpResponse('Password reset link is invalid or has expired.')


class Password_ResetView_confirm_token(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            profile = Profile.objects.get(reset_password_token=token)
            user = profile.user
            user.set_password(new_password)
            profile.reset_password_token = None
            profile.save()

            user.save()
            return render(request, 'reset_password.html', {'success_message': 'Password has been reset successfully.'})

            # Handle serializer errors
        return render(request, 'reset_password.html',{'error_message': 'Invalid data provided for password reset.'})
