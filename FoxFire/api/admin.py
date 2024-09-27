from django.contrib import admin
from .models import (
    Task,
    Category,
    Question,
    WithdrawRequest,
    ExchangeRate,
    Survey,
    Referral,
    SurveyCompletion,
    UserResponse,
)
from wallet.models import Wallet, Transaction

# Register your models here.
admin.site.register(
    [
        Task,
        Category,
        Question,
        WithdrawRequest,
        SurveyCompletion,
        UserResponse,
        Survey,
        ExchangeRate,
        Wallet,
        Transaction,
        Referral,
    ]
)
