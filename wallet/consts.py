from django.db.models import TextChoices

from django.utils.translation import gettext_lazy as _


class TransactionChoices(TextChoices):
    DEPOSIT = 'deposit', _('deposit')
    WITHDRAW = 'withdraw', _('withdraw')
    PURCHASE = 'purchase', _('purchase')
