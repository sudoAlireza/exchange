import logging
from decimal import Decimal

from django.db.models import Sum

from order.consts import OrderStatusChoices, OrderTypeChoices
from order.exceptions import ExchangeNotRespond
from order.exchanges.binance import Binance
from order.models import Order


logger = logging.getLogger("order-handler")


class OrderHandler:
    @staticmethod
    def process_order(user, currency_code, amount, total_cost):
        logger.info("Starting order processing for user %s, currency %s, amount %s, total cost %s",
                    user.id, currency_code, amount, total_cost)

        new_order = OrderHandler._create_new_order(user, currency_code, amount)
        total_amount = OrderHandler._calculate_total_amount(currency_code)

        if total_amount >= Decimal("10"):
            return OrderHandler._process_exchange(new_order, currency_code, total_amount)

        logger.info("Total amount less than 10, order created in PENDING status.")
        return "Order created as PENDING.", new_order

    @staticmethod
    def _create_new_order(user, currency_code, amount):
        logger.debug("Creating new order for user %s with currency %s", user.id, currency_code)

        return Order.objects.create(
            user=user,
            order_type=OrderTypeChoices.BUY,
            currency_pair=f"USD/{currency_code}",
            price=Decimal("4"),
            amount=amount,
            status=OrderStatusChoices.PENDING,
        )

    @staticmethod
    def _calculate_total_amount(currency_code):
        logger.debug("Calculating total amount for pending orders.")
        current_pending_sum = Order.objects.filter(
            currency_pair=f"USD/{currency_code}",
            status=OrderStatusChoices.PENDING,
        ).aggregate(total_amount=Sum("amount"))["total_amount"] or Decimal("0")

        total_cost = current_pending_sum * Decimal("4")  
        logger.debug("Current pending sum: %s, total cost: %s", current_pending_sum, total_cost)

        return total_cost

    @staticmethod
    def _process_exchange(new_order, currency_code, total_amount):
        logger.info("Attempting to process exchange for total amount: %s", total_amount)

        try:
            
            Binance.buy_from_exchange(currency_code=currency_code, amount=total_amount)
            OrderHandler._mark_orders_as_succeeded(currency_code)

            new_order.status = OrderStatusChoices.SUCCEEDED
            new_order.save()

            logger.info("Buy request sent and orders marked as COMPLETED.")
            return "Buy request sent and orders marked as COMPLETED.", new_order

        except ExchangeNotRespond:
            logger.error("Error connecting to Binance exchange. ExchangeNotRespond.")
            raise ExchangeNotRespond("Error connecting to Binance exchange.")

        except Exception as e:
            logger.error(f"Unexpected error while processing order: {e}")
            raise ValueError(f"Error processing order: {e}")

    @staticmethod
    def _mark_orders_as_succeeded(currency_code):
        logger.debug("Marking all pending orders as SUCCEEDED.")
        Order.objects.filter(
            currency_pair=f"USD/{currency_code}",
            status=OrderStatusChoices.PENDING,
        ).update(status=OrderStatusChoices.SUCCEEDED)
