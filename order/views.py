import logging

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


logger = logging.getLogger("order-views")
class PurchaseOrderView(APIView):

    @extend_schema(
        request=PurchaseOrderSerializer,
        responses={201: OrderSerializer},
    )
    def post(self, request):
        logger.info("Received POST request for PurchaseOrderView.")
        serializer = PurchaseOrderSerializer(data=request.data)

        if not serializer.is_valid():
            logger.error("Invalid data received: %s", serializer.errors)
            serializer.is_valid(raise_exception=True)

        currency_code = serializer.validated_data["currency_code"]
        amount = serializer.validated_data["amount"]
        user = request.user

        logger.info("Processing purchase for user %s with currency %s and amount %s", user, currency_code, amount)

        currency = get_object_or_404(Currency, code=currency_code)
        wallet = get_object_or_404(Wallet, user=user, currency=currency)

        total_cost = currency.price * amount
        logger.debug("Calculated total cost: %s", total_cost)

        try:
            with transaction.atomic():
                logger.info("Adjusting wallet balance.")
                wallet.adjust_balance(amount, TransactionChoices.PURCHASE)
                logger.info("Processing order.")
                message, order = OrderHandler.process_order(
                    user, currency_code, amount, total_cost
                )

            if order:
                logger.info("Order created successfully with ID: %s", order.id)
            else:
                logger.warning("Order creation failed.")

            return Response(
                {"detail": message, "order_id": order.id if order else None},
                status=(
                    status.HTTP_201_CREATED
                    if order
                    else status.HTTP_500_INTERNAL_SERVER_ERROR
                ),
            )

        except Exception as e:
            logger.exception("Error occurred during order processing.")
            return Response(
                {"detail": "An error occurred. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )