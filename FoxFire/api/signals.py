from django.conf import settings
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from wallet.models import Wallet
from .models import Referral
User = settings.AUTH_USER_MODEL


@receiver(post_save, sender=User)
def create_profile_on_save(sender, instance: User, created, *args, **kwargs):
    # generate wallet for user if no wallet exists
    if not instance.wallet_set.exists():
        instance.wallet_set.create()
    if not instance.referral_set.exists():
        Referral.objects.create(user = instance).save()



# TODO send email to user on account create
# TODO send email to user when a task OR anouncment is created
