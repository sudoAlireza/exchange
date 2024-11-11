from decimal import Decimal

from django.db.models import Sum

from order.consts import OrderStatusChoices, OrderTypeChoices
from order.exchanges.binance import Binance
from order.models import Order


class OrderHandler:
    @staticmethod
    def process_order(user, currency_code, amount, total_cost):

        new_order = Order.objects.create(
            user=user,
            order_type=OrderTypeChoices.BUY,
            currency_pair="USD/ABAN",
            price=Decimal("4"),
            amount=amount,
            status=OrderStatusChoices.PENDING,
        )

        current_pending_sum = Order.objects.filter(
            currency_pair="USD/ABAN",
            status=OrderStatusChoices.PENDING,
        ).aggregate(total_amount=Sum("amount"))["total_amount"] or Decimal("0")

        total_amount = (current_pending_sum * 4) + total_cost

        if total_amount >= Decimal("10"):
            try:
                Binance.buy_from_exchange(
                    currency_code=currency_code, amount=total_amount
                )

                Order.objects.filter(
                    currency_pair="USD/ABAN",
                    status=OrderStatusChoices.PENDING,
                ).update(status=OrderStatusChoices.SUCCEEDED)
                new_order.status = OrderStatusChoices.SUCCEEDED
                new_order.save()

                return "Buy request sent and orders marked as COMPLETED.", new_order

            except Exception as e:

                raise ValueError("Error processing order: {e}")

        else:
            return "Order created as PENDING.", new_order
