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


class WalletAddressViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = WalletAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WalletAddress.objects.filter(
            wallet__user=self.request.user
        ).prefetch_related("wallet__currency")

    def perform_create(self, serializer):
        currency_code = self.request.data.get("currency_code")
        currency = get_object_or_404(Currency, code=currency_code)
        wallet, _ = Wallet.objects.get_or_create(
            user=self.request.user, currency=currency
        )

        validated_data = serializer.validated_data
        validated_data.pop("currency_code", None)

        serializer.save(wallet=wallet)


class WalletDepositWithdrawViewSet(GenericViewSet):
    queryset = Wallet.objects.all()
    serializer_class = DepositWithdrawSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.wallets.all()

    @transaction.atomic
    @action(detail=False, methods=["post"], url_path="deposit")
    def deposit(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        currency_code = serializer.validated_data["currency_code"]
        amount = serializer.validated_data["amount"]
        user = request.user

        currency = get_object_or_404(Currency, code=currency_code)
        wallet, _ = Wallet.objects.prefetch_related("addresses").get_or_create(
            user=user, currency=currency
        )

        if not wallet.addresses.exists():
            WalletAddress.objects.create(wallet=wallet)

        wallet.adjust_balance(amount, TransactionChoices.DEPOSIT)

        return Response(
            {"message": "Deposit successful", "balance": wallet.balance},
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    @action(detail=False, methods=["post"], url_path="withdraw")
    def withdraw(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        currency_code = serializer.validated_data["currency_code"]
        amount = serializer.validated_data["amount"]
        user = request.user

        wallet = get_object_or_404(Wallet, user=user, currency__code=currency_code)
        wallet.adjust_balance(-amount, TransactionChoices.WITHDRAW)

        return Response(
            {"message": "Withdrawal successful", "balance": wallet.balance},
            status=status.HTTP_200_OK,
        )
