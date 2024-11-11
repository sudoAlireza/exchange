from django.conf import settings
from rest_framework import status

from order.exceptions import ExchangeNotRespond
from order.exchanges.exchanges_interface import AbstractExchange


class Binance(AbstractExchange):

    @classmethod
    def set_order(cls, currency_code, amount):

        #mock http requst:
        # url = settings.BINANCE_BUY_CURRENCY_API or 'test'
        # headers = {"Content-Type": "application/json", "Authorization": f"Bearer {settings.BINANCE_API_KEY or 'test'}"}
        # data = {"currency": currency_code, "amount": amount}
        status_code, request_respone = 201, {"result": "ok"}

        if status.HTTP_200_OK <= status_code < status.HTTP_300_MULTIPLE_CHOICES:
            return {
                "error": None,
                "status_code": status_code,
                "response": request_respone
            }
        
        else:
            #TODO: handle 4xx errors and 5xx errors separately
            raise ExchangeNotRespond()

    @classmethod
    def buy_from_exchange(cls, currency_code, amount)-> dict:
        return cls.set_order(currency_code, amount)