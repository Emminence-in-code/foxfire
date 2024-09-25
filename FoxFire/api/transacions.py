from django.db import transaction
from wallet.models import Wallet
from wallet.errors import InsufficientBalance


def deposit(wallet: Wallet, amount: int):
    with transaction.atomic():
        wallet.deposit(amount)


def withdraw(wallet: Wallet, amount: int) -> bool:
    try:
        with transaction.atomic():
            wallet.withdraw(amount)
            return True
            
    except InsufficientBalance:
        return False
