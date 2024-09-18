from custom_auth.models import CustomUser
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    BaseSerializer,
)
from custom_auth.validators import validate_username


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
    class Meta:
        model = CustomUser
        exclude = ("id", "password")
