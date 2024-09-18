from django.shortcuts import render
from custom_auth.models import CustomUser
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import views
from rest_framework import status
from django.shortcuts import render
from api.serializers import UserSerializer

# from django.contrib.auth import
from custom_auth.models import CustomUser
from rest_framework import generics, decorators
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views, decorators
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import (
    Task,
    Category,
    Survey,
    Question,
    UserResponse,
    SurveyCompletion,
    Announcement,
    WithdrawRequest,
    ExchangeRate,
)
from .serializers.serializers import (
    TaskSerializer,
    CategorySerializer,
    SurveySerializer,
    QuestionSerializer,
    UserResponseSerializer,
    SurveyCompletionSerializer,
    AnnouncementSerializer,
    WithdrawRequestSerializer,
    ExchangeRateSerializer,
)

from api.serializers import UserSerializer


# Create your views here.


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        if CustomUser.objects.filter(username=request.data.get("username")).exists():
            return Response(
                {"error": "username already exists"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if CustomUser.objects.filter(username=request.data.get("email")).exists():
            return Response(
                {"error": "Account with email already exists"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = super().post(request, *args, **kwargs)
        user_data = response.data
        # Get the user instance for token generation
        try:
            user_obj = CustomUser.objects.get(email=user_data.get("email"))
            # Generate tokens
            token_pair = RefreshToken.for_user(user_obj)
            response_data: dict = {
                "refresh": str(token_pair),
                "access": str(token_pair.access_token),
                "username": user_obj.username,
                "email": user_obj.email,
                "image": "",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_400_BAD_REQUEST
            )


class GetUserApiView(RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = ""

    def get_queryset(self):
        # Return a queryset with just the authenticated user
        return self.request.user

    def get_object(self):
        # Get the first object from the queryset
        queryset = self.get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        # Handle GET request
        return self.retrieve(request, *args, **kwargs)


class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "username": user.username,
                "email": user.email,
                "profile_picture": user.profile_picture if user.profile_picture else "",
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


# views for adding tasks


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


class UserResponseViewSet(viewsets.ModelViewSet):
    queryset = UserResponse.objects.all()
    serializer_class = UserResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserResponse.objects.filter(user=self.request.user)


class SurveyCompletionViewSet(viewsets.ModelViewSet):
    queryset = SurveyCompletion.objects.all()
    serializer_class = SurveyCompletionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SurveyCompletion.objects.filter(user=self.request.user)


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]


class WithdrawRequestViewSet(viewsets.ModelViewSet):
    queryset = WithdrawRequest.objects.all()
    serializer_class = WithdrawRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WithdrawRequest.objects.filter(user=self.request.user)


class ExchangeRateViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]
