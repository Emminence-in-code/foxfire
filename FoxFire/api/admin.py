from django.contrib import admin
from .models import (
    Task,
    Announcement,
    Category,
    Question,
    WithdrawRequest,
    ExchangeRate,
)


# Register your models here.
admin.site.register(
    [
        Task,
        Announcement,
        Category,
        Question,
        WithdrawRequest,
        ExchangeRate,
    ]
)
