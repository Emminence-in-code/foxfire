from rest_framework.views import APIView
from django.shortcuts import render
from custom_auth.models import CustomUser
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import views
from rest_framework import status
from django.shortcuts import render
from api.serializers import UserSerializer
from notifications_and_messages.models import send_notification
from .transacions import deposit, withdraw
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework.parsers import MultiPartParser, FormParser

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
from django.db.models import Exists, OuterRef
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from wallet.models import Wallet
from .models import (
    Task,
    Category,
    Referral,
    Survey,
    Question,
    UserResponse,
    SurveyCompletion,
    WithdrawRequest,
    ExchangeRate,
    TaskSubmit,
)
from .serializers.serializers import (
    TaskSerializer,
    CategorySerializer,
    SurveySerializer,
    QuestionSerializer,
    UserResponseSerializer,
    SurveyCompletionSerializer,
    TaskSubmitSerializer,
    WithdrawRequestSerializer,
    ExchangeRateSerializer,
)

from api.serializers.UserSerializer import UserSerializer, UserDetailSerializer

import random

# Create your views here.


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    authentication_classes = []
    permission_classes = []

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
            # handle referrer
            try:
                if request.data.get("referral_code"):
                    ref = Referral.objects.get(code=request.data.get("referral_code"))
                    ref.use_code()
                    deposit(ref.user.wallet_set.first(), 100)
                    send_notification(
                        title="Invitation accepted",
                        user=ref.user,
                        notification=f"{user_obj.username} accepted your invitation and has used your referral code",
                    )
            except:
                pass

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
    authentication_classes = []
    permission_classes = []

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
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]
    queryset = Survey.objects.filter(upload_complete=True)

    def get_queryset(self):
        user = self.request.user
        return Survey.objects.filter(
            ~Exists(
                SurveyCompletion.objects.filter(
                    user=user, survey=OuterRef("pk"), completed=True
                )
            )
        )


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


class TaskSubmitViewSet(viewsets.ModelViewSet):
    queryset = TaskSubmit.objects.all()
    serializer_class = TaskSubmitSerializer
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


class WithdrawRequestViewSet(viewsets.ModelViewSet):
    queryset = WithdrawRequest.objects.all()
    serializer_class = WithdrawRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WithdrawRequest.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Deserialize and validate the incoming data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the validated data and the user's wallet
        data = serializer.validated_data
        user_wallet = self.request.user.wallet_set.first()
        if data.get("amount") == 0:
            return Response({"error": "cant withdraw zero balance"}, status=400)
        # Perform the withdrawal action
        x = withdraw(user_wallet, data.get("amount"))

        # Check the withdrawal result and return the appropriate response
        if x:
            # If withdrawal is successful, save the serializer
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If withdrawal fails, return an error response
            return Response(
                {"error": "Insufficient balance"}, status=status.HTTP_403_FORBIDDEN
            )


class ExchangeRateViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]


class GetUserApiView(RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = UserDetailSerializer
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


class DeleteUserAccountView(APIView):
    """
    GET endpoint to delete the currently authenticated user's account.
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        CustomUser.objects.get(username=user.username).delete()
        return Response(
            {"message": "User account deleted successfully."}, status=status.HTTP_200_OK
        )


class SubmitSurveyResponse(APIView):
    def post(self, request, survey_id):
        survey = get_object_or_404(Survey, id=survey_id)
        user = request.user

        # Expect a dictionary of question_id: answer pairs
        answers = request.data.get("answers", {})

        answered_questions_count = 0  # Counter for the current answered questions

        for question_id, answer in answers.items():
            question = survey.questions.filter(id=question_id).first()
            if question and answer:
                # Update or create the user response
                UserResponse.objects.update_or_create(
                    user=user, question=question, defaults={"answer": answer}
                )
                answered_questions_count += 1  # Increment count for each valid answer

        # Check if all questions in the survey are answered
        total_questions = survey.questions.count()

        completion, _ = SurveyCompletion.objects.get_or_create(user=user, survey=survey)
        if (
            total_questions == answered_questions_count
        ):  # Compare only with current answers
            completion.completed = True
            completion.completed_at = timezone.now()
            completion.save()
            # Fund user for completing the survey
            user_wallet: Wallet = user.wallet_set.first()
            deposit(user_wallet, survey.reward)
            send_notification(
                user=user,
                title="Survey Completed",
                notification=f"Survey completed you have earned {survey.reward} for this survey",
            )
            return Response(
                {"completed": True, "answered_questions": answered_questions_count},
                status=200,
            )

        completion.save()
        return Response(
            {"completed": False, "answered_questions": answered_questions_count},
            status=200,
        )


class GetAdsRewardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_wallet = request.user.wallet_set.first()
        reward = random.randint(10, 100)
        deposit(user_wallet, reward)
        send_notification(
            title="Ads Rewarded",
            user=self.request.user,
            notification="You have earned from watching ads,check your balance",
        )
        return Response()


class ProfileImageUpdateView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        serializer = UserDetailSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
