import logging
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from currency.models import Currency
from wallet.consts import TransactionChoices
from wallet.models import Wallet, WalletAddress
from wallet.serializers import DepositWithdrawSerializer, WalletAddressSerializer

logger = logging.getLogger("wallet-views")

class WalletAddressViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = WalletAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        logger.info("Fetching wallet addresses for user: %s", user)
        return WalletAddress.objects.filter(
            wallet__user=user
        ).prefetch_related("wallet__currency")

    def perform_create(self, serializer):
        currency_code = self.request.data.get("currency_code")
        logger.info("Creating wallet address for user: %s with currency: %s", self.request.user, currency_code)
        currency = get_object_or_404(Currency, code=currency_code)
        wallet, created = Wallet.objects.get_or_create(
            user=self.request.user, currency=currency
        )
        if created:
            logger.info("New wallet created for user: %s with currency: %s", self.request.user, currency_code)

        validated_data = serializer.validated_data
        validated_data.pop("currency_code", None)

        serializer.save(wallet=wallet)
        logger.info("Wallet address created successfully for user: %s", self.request.user)


class WalletDepositWithdrawViewSet(GenericViewSet):
    queryset = Wallet.objects.all()
    serializer_class = DepositWithdrawSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        logger.info("Fetching wallets for user: %s", user)
        return user.wallets.all()

    @transaction.atomic
    @action(detail=False, methods=["post"], url_path="deposit")
    def deposit(self, request, *args, **kwargs):
        logger.info("Received deposit request for user: %s", request.user)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Invalid deposit data for user: %s, errors: %s", request.user, serializer.errors)
            serializer.is_valid(raise_exception=True)

        currency_code = serializer.validated_data["currency_code"]
        amount = serializer.validated_data["amount"]
        user = request.user

        logger.info("Processing deposit for user: %s, currency: %s, amount: %s", user, currency_code, amount)
        currency = get_object_or_404(Currency, code=currency_code)
        wallet, created = Wallet.objects.prefetch_related("addresses").get_or_create(
            user=user, currency=currency
        )
        if created:
            logger.info("New wallet created for deposit for user: %s", user)

        if not wallet.addresses.exists():
            logger.info("No wallet address found, creating a new one for user: %s", user)
            WalletAddress.objects.create(wallet=wallet)

        wallet.adjust_balance(amount, TransactionChoices.DEPOSIT)
        logger.info("Deposit successful for user: %s, new balance: %s", user, wallet.balance)

        return Response(
            {"message": "Deposit successful", "balance": wallet.balance},
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    @action(detail=False, methods=["post"], url_path="withdraw")
    def withdraw(self, request, *args, **kwargs):
        logger.info("Received withdrawal request for user: %s", request.user)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Invalid withdrawal data for user: %s, errors: %s", request.user, serializer.errors)
            serializer.is_valid(raise_exception=True)

        currency_code = serializer.validated_data["currency_code"]
        amount = serializer.validated_data["amount"]
        user = request.user

        logger.info("Processing withdrawal for user: %s, currency: %s, amount: %s", user, currency_code, amount)
        wallet = get_object_or_404(Wallet, user=user, currency__code=currency_code)
        wallet.adjust_balance(-amount, TransactionChoices.WITHDRAW)
        logger.info("Withdrawal successful for user: %s, new balance: %s", user, wallet.balance)

        return Response(
            {"message": "Withdrawal successful", "balance": wallet.balance},
            status=status.HTTP_200_OK,
        )
