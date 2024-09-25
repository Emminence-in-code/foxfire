from .models import CustomUser
from rest_framework import serializers
from django.utils.text import slugify


def validate_username(value: str):
    # ! strip every whitespace from the 'value' variable
    value = slugify(value)
    query = CustomUser.objects.filter(username__iexact=value)
    if query.exists():
        raise serializers.ValidationError("Username already exists")
    if " " in value:
        raise serializers.ValidationError("Username cannot contain spaces")
    if len(value) < 8:
        raise serializers.ValidationError("Username cannot be less than 8 characters")
    for i in ["!", "$", "%", "*", "&"]:
        if i in value:
            raise serializers.ValidationError(
                "Username cannot contain invalid characters"
            )
    return value
