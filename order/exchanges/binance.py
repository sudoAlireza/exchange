import logging
from decimal import Decimal

from django.conf import settings
from django.db import transaction
from rest_framework import status
from order.exceptions import ExchangeNotRespond
from order.exchanges.exchanges_interface import AbstractExchange

# Configure logger for this module
logger = logging.getLogger("binance-exchange")


class Binance(AbstractExchange):
    """Handles interactions with the Binance exchange."""

    @classmethod
    def set_order(cls, currency_code: str, amount: Decimal) -> dict:

        logger.info("Preparing to set an order for currency: %s, amount: %s", currency_code, amount)

        # mock HTTP request
        url = settings.BINANCE_BUY_CURRENCY_API or 'test'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.BINANCE_API_KEY or 'test'}"
        }
        data = {"currency": currency_code, "amount": amount}

        logger.debug("Mock HTTP request to URL: %s with headers: %s and data: %s", url, headers, data)

        # ,ock HTTP response
        status_code, response_data = 201, {"result": "ok"}

        if status.HTTP_200_OK <= status_code < status.HTTP_300_MULTIPLE_CHOICES:
            logger.info("Order set successfully with status code: %s", status_code)
            return {
                "error": None,
                "status_code": status_code,
                "response": response_data
            }
        else:
            logger.error("Failed to set order. Status code: %s, Response: %s", status_code, response_data)
            # TODO: implement more better error handling for 4xx and 5xx errors
            raise ExchangeNotRespond(f"Failed to communicate with Binance API. Status code: {status_code}")

    @classmethod
    def buy_from_exchange(cls, currency_code, amount) -> dict:

        logger.info("Initiating buy operation for currency: %s, amount: %s", currency_code, amount)

        try:
            response = cls.set_order(currency_code, amount)
            logger.info("Buy operation successful. Response: %s", response)
            return response

        except ExchangeNotRespond as ex:
            logger.error("ExchangeNotRespond error: %s", ex)
            transaction.set_rollback(True)
            raise

        except Exception as e:
            logger.exception("An unexpected error occurred while buying from Binance: %s", e)
            transaction.set_rollback(True)
            raise RuntimeError("Transaction failed due to an unexpected error.") from e
