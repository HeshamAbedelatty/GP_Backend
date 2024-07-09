from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer, LogoutSerializer
from django.contrib.auth import authenticate
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = UserSerializer(user).data
        try:
            email_user = 'mohamed9999ah@gmail.com'
            email_password = 'mdhmvhapwmpiaued'
            email_send = user.email

            subject = 'Welcome Email'

            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_send
            msg['Subject'] = subject
            # send data by html file to email
            body = f"Hello {user.username},\n\nWelcome to our platform. Your account has been created successfully.\n\nBest regards,\nSa3teenGd Team"
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)
            text = msg.as_string()
            server.sendmail(email_user, email_send, text)
            server.quit()
            return Response(user_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer  # Just for validation, won't actually use it

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'is_active': user.is_active,
            })
        else:
            return Response({'error': 'Invalid Credentials'}, status=400)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh']
        
        # try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "LogOut successfully"},status=status.HTTP_205_RESET_CONTENT)
        # except Exception as e:
        #     return Response({},status=status.HTTP_400_BAD_REQUEST)

# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()

#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
