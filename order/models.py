from django.db import models

from core.utils import BaseTimestampedModel
from order.consts import OrderStatusChoices, OrderTypeChoices


class Order(BaseTimestampedModel):

    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="orders"
    )
    order_type = models.CharField(max_length=4, choices=OrderTypeChoices)
    status = models.CharField(
        max_length=20, choices=OrderStatusChoices, default=OrderStatusChoices.REQUESTED
    )
    currency_pair = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    amount = models.DecimalField(max_digits=20, decimal_places=8)

    class Meta:
        indexes = [models.Index(fields=["currency_pair", "order_type", "status"])]

    def __str__(self) -> str:
        return f"{self.order_type} {self.amount} {self.currency_pair} @ {self.price}"


#TODO: the better way to do this part is create Market model with pair currencies
# and in Order class we would have two separate field related to currency model
# also it's better to create a job to check prices from exchanges APIs and store in cache
# in buy orders we could fetch and sort them, then with Strategy design pattern run `buy_from_exchange` method for exchanges that have same abstract class
# also I added `sell_to_exchange` method to `AbstractExchange` but not implemented