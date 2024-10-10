from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from wallet.models import Wallet

from api.transacions import deposit
from .models import Referral
from api.models import WithdrawRequest, ExchangeRate, Task, Survey
from custom_auth.models import CustomUser

User = settings.AUTH_USER_MODEL
from notifications_and_messages.models import send_notification


@receiver(post_save, sender=CustomUser)
def create_profile_on_save(sender, instance: CustomUser, created, *args, **kwargs):
    if not instance.wallet_set.exists():
        instance.wallet_set.create()
    if not instance.referral_set.exists():
        Referral.objects.create(user=instance).save()
    if created:
        send_notification(
            f"Welcome {instance.username}",
            instance,
            "Your sign up has been completed succesfully,start taking surveys to earn flame tokens",
        )


@receiver(post_save, sender=Task)
def notify_user_of_new_task(sender, instance, created, *args, **kwargs):
    # notify all users
    if created:
        users = CustomUser.objects.all()
        for user in users:
            send_notification(
                title="There's a new task",
                user=user,
                notification="Hey there, there is a new task. complete task and earn flame tokens",
            )


@receiver(post_save, sender=Survey)
def notify_user_of_new_survey(sender, instance: Survey, created, *args, **kwargs):
    if instance.upload_complete:
        # notify all users
        users = CustomUser.objects.all()
        for user in users:
            send_notification(
                title="New Survey",
                user=user,
                notification="Why wait when you can start earning,checkout the new survey",
            )


@receiver(post_save, sender=WithdrawRequest)
def notify_withdraw_request(
    sender, instance: WithdrawRequest, created, *args, **kwargs
):
    if created:
        send_notification(
            title="Withdraw Request sent",
            user=instance.user,
            notification="Your withdraw request has been sent,your funds will be transfered to your account within 3 days",
        )
    if instance.confirmed:
        send_notification(
            title="Withdraw Request Confirmed",
            user=instance.user,
            notification="Your withdraw request has been Confirmed,you will now recieve your funds",
        )


@receiver(post_delete, sender=WithdrawRequest)
def delete_withdraw_request(sender, instance: WithdrawRequest, *args, **kwargs):
    if not instance.confirmed:
        send_notification(
            title="Withdraw Request Denied",
            user=instance.user,
            notification=f"Unfortunately u cannot withdraw at this moment,{instance.amount} will be returned to your wallet"
        )
        # send back funds to user
        deposit(amount=instance.amount, wallet=instance.user.wallet_set.first())


@receiver(post_save, sender=ExchangeRate)
def notify_rates_request(sender, instance: ExchangeRate, created, *args, **kwargs):
    users = CustomUser.objects.all()
    for user in users:
        send_notification(
            title="Update in Rates",
            user=user,
            notification="Exchange rates has been updated,check it out to see if its in your favour",
        )
