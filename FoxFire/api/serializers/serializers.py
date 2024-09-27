from rest_framework import serializers
from api.models import (
    Task,
    Category,
    Survey,
    Question,
    UserResponse,
    SurveyCompletion,
    WithdrawRequest,
    ExchangeRate,TaskSubmit
)
from .UserSerializer import UserSerializer as CustomUserSerializer


class TaskSerializer(serializers.ModelSerializer):
    completed = CustomUserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    total_questions = serializers.SerializerMethodField()
    answered_questions = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = "__all__"

    def get_total_questions(self, obj):
        return obj.get_total_questions_count()

    def get_answered_questions(self, obj):
        user = self.context["request"].user
        return obj.get_answered_questions_count(user)


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = "__all__"


class SurveyCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyCompletion
        fields = "__all__"



class WithdrawRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawRequest
        fields = "__all__"


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = "__all__"


class TaskSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSubmit
        fields = "__all__"

