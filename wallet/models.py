from django.db import models, transaction
from django.core.validators import MinValueValidator

from core.utils import BaseTimestampedModel, generate_wallet_address
from decimal import Decimal

from currency.models import Currency
from order.exceptions import InsufficientBalance
from order.models import Order
from wallet.consts import TransactionChoices


class Wallet(BaseTimestampedModel):
    user = models.ForeignKey(
        "user.User", on_delete=models.PROTECT, related_name="wallets"
    )
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="wallet")
    balance = models.DecimalField(
        max_digits=20, decimal_places=8, default=0, validators=[MinValueValidator(0)]
    )

    class Meta:
        unique_together = ("user", "currency")

    def __str__(self):
        return f"{self.user.username}'s {self.currency.code} Wallet"

    def _create_transaction(
        self, amount, transaction_type, related_address=None, details=None
    ):

        transaction = Transaction.objects.create(
            wallet=self,
            amount=amount,
            transaction_type=transaction_type,
            related_address=related_address,
        )
        return transaction

    def _create_transaction_log(self, transaction, previous_balance, details=None):

        TransactionLog.objects.create(
            transaction=transaction,
            previous_balance=previous_balance,
            new_balance=self.balance,
            details=details or {},
        )

    @transaction.atomic()
    def adjust_balance(
        self, amount: Decimal, transaction_type, related_address=None, details=None
    ):
        if self.balance + amount < 0:
            raise InsufficientBalance()

        previous_balance = self.balance
        self.balance += amount

        transaction = self._create_transaction(
            amount, transaction_type, related_address
        )
        self._create_transaction_log(transaction, previous_balance)
        self.save()


class WalletAddress(models.Model):
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="addresses"
    )
    address = models.CharField(
        max_length=100, unique=True, default=generate_wallet_address
    )

    def __str__(self):
        return f"Address: {self.address} (Wallet: {self.wallet})"


class Transaction(BaseTimestampedModel):
    wallet = models.ForeignKey(
        Wallet, on_delete=models.PROTECT, related_name="transactions"
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.SET_NULL,
        related_name="transaction",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    transaction_type = models.CharField(max_length=20, choices=TransactionChoices)
    related_address = models.ForeignKey(
        WalletAddress,
        on_delete=models.SET_NULL,
        related_name="transactions",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]


class TransactionLog(BaseTimestampedModel):
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="logs"
    )
    previous_balance = models.DecimalField(max_digits=20, decimal_places=8)
    new_balance = models.DecimalField(max_digits=20, decimal_places=8)
    details = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Log for Transaction: {self.transaction.id}"
