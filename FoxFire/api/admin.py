from django.contrib import admin
from .models import (
    Task,
    Announcement,
    Category,
    Question,
    WithdrawRequest,
    ExchangeRate,
    Survey,
)


# Register your models here.
admin.site.register(
    [
        Task,
        Announcement,
        Category,
        Question,
        WithdrawRequest,
        Survey,
        ExchangeRate,
    ]
)
