from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Model for custom user of my app , including firstname ,lastname, phone number,date of birth, state of origin , state of residence and profile picture
    """

    username = models.CharField(max_length=100)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(null=True, blank=True, max_length=200)
    first_name = models.CharField(null=True, blank=True, max_length=200)
    last_name = models.CharField(null=True, blank=True, max_length=200)
    verified_phone_number = models.BooleanField(default=False)
    verified_email_address = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to="files")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    objects = CustomUserManager()

    # Specify related_name to avoid clashes with auth.User
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name=_("groups"),
        blank=True,
        related_name="custom_user_set",  # Custom related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name=_("user permissions"),
        blank=True,
        related_name="custom_user_set",  # Custom related_name
        related_query_name="user",
    )

    def __str__(self) -> str:
        return self.email

    @property
    def is_verified_user(self):
        return self.verified_email_address and self.verified_phone_number
