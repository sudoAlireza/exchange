from django.db.models import TextChoices

from django.utils.translation import gettext_lazy as _


class OrderStatusChoices(TextChoices):
    REQUESTED = "requested", _("requested")
    PENDING = "pending", _("pending")
    SUCCEEDED = "succeeded", _("succeeded")
    FAILED = "failed", _("failed")


class OrderTypeChoices(TextChoices):
    BUY = "buy", _("buy")
    SELL = "sell", _("sell")
