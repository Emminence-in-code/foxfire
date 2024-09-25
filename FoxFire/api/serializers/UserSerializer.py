from custom_auth.models import CustomUser
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    BaseSerializer,
)
from custom_auth.validators import validate_username
from wallet.models import Wallet
from api.models import *


class UserSerializer(ModelSerializer):
    username = CharField(validators=[validate_username])

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "password",
        ]

    def create(self, validated_data):
        username = validated_data.get("username", None)
        if username != None and " " in username:
            username = username.replace(" ", "")
        validated_data["username"] = username
        password = validated_data.pop("password")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(ModelSerializer):
    balance = SerializerMethodField()
    completed_tasks_count = SerializerMethodField()
    completed_surveys_count = SerializerMethodField()
    referrers_count = SerializerMethodField()
    referral_code = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_picture",
            "is_staff",
            "balance",
            "completed_tasks_count",
            "completed_surveys_count",
            "referrers_count",
            "referral_code",
        ]

    def get_balance(self, instance):
        wallet: Wallet = instance.wallet_set.first()
        return wallet.current_balance

    def get_completed_tasks_count(self, obj):
        return Task.objects.filter(completed=obj).count()

    def get_completed_surveys_count(self, obj):
        return SurveyCompletion.get_completed_surveys_count(obj)

    def get_referrers_count(self, obj):
        return Referral.objects.filter(user=obj).first().used_count

    def get_referral_code(self, obj):
        return Referral.objects.filter(user=obj).first().code
