from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from currency.models import Currency
from order.serializers import OrderSerializer, PurchaseOrderSerializer
from order.services.order import OrderHandler
from wallet.models import Wallet, TransactionChoices

from drf_spectacular.utils import extend_schema


class PurchaseOrderView(APIView):

    @extend_schema(
        request=PurchaseOrderSerializer,
        responses={201: OrderSerializer},
    )
    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        currency_code = serializer.validated_data["currency_code"]
        amount = serializer.validated_data["amount"]
        user = request.user

        currency = get_object_or_404(Currency, code=currency_code)
        wallet = get_object_or_404(Wallet, user=user, currency=currency)

        total_cost = currency.price * amount

        with transaction.atomic():
            wallet.adjust_balance(amount, TransactionChoices.PURCHASE)
            message, order = OrderHandler.process_order(
                user, currency_code, amount, total_cost
            )

        return Response(
            {"detail": message, "order_id": order.id if order else None},
            status=(
                status.HTTP_201_CREATED
                if order
                else status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
        )
