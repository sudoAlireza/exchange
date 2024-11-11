from django.db import models
import uuid


def generate_wallet_address():
    """Generate a unique wallet address using UUID."""
    return str(uuid.uuid4()).replace('-', '')


class BaseTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True