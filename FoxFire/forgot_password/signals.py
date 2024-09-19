from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.mails import send_password_token
from .models import Token


def generate_mail_template(token):
    mail_template: str = settings.FORGOT_PASSWORD_CONFIG.get("mail_template")
    if mail_template and "#token" in mail_template:
        return mail_template.replace("#token", token)
    else:
        return


@receiver(post_save, sender=Token)
def handle_token_created(sender, instance: Token, created, *args, **kwargs):
    send_password_token(instance.user.username, instance.token, instance.user.email)
