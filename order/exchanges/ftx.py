from django.conf import settings
from rest_framework import status

from order.exceptions import ExchangeNotRespond
from order.exchanges.exchanges_interface import AbstractExchange


class FTX(AbstractExchange):
    pass