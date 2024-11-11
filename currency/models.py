from django.db import models

from core.utils import BaseTimestampedModel


class Currency(BaseTimestampedModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=20, decimal_places=8, null=True, default=0)

    def __str__(self) -> str:
        return self.code
