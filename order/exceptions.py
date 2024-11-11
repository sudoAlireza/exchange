from django.utils.translation import gettext_lazy as _
from rest_framework import status

from rest_framework.exceptions import APIException


class InsufficientBalance(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Your wallet balance is not enough")
    default_code = 0xAD01


class ExchangeNotRespond(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = _("The exchange doesn't respond")
    default_code = 0xAD02


class PurchaseNotSuccessful(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Purchase transaction failed")
    default_code = 0xAD03