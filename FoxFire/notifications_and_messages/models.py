from collections.abc import Iterable
from datetime import datetime, timedelta, timezone

from django.db import models
from custom_auth.models import CustomUser as User
from helpers.format_date import format_time_ago


# Create your models here.
#  todo ALSO DISPLAY NOTIFICATION TYPE
class Notifications(models.Model):
    notification = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    @property
    def formated_time(self):
        return format_time_ago(self.created_at)

    def mark_as_read(self):
        self.read = True
        self.save()


class Messages(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    reciever = models.CharField(max_length=200,default='admin')
    # todo should be created based on the contetatenation of the two users in the chat as a slug or the name of the group or room holding a meeting
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def read(self):
        self.read = True
        self.save()
