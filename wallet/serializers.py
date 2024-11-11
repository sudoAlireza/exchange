from rest_framework import serializers
from decimal import Decimal

from wallet.models import WalletAddress


class DepositWithdrawSerializer(serializers.Serializer):
    currency_code = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(
        max_digits=20, decimal_places=8, min_value=Decimal("0.00000001")
    )


class WalletAddressSerializer(serializers.ModelSerializer):
    currency_code = serializers.CharField(source="wallet.currency.code")

    class Meta:
        model = WalletAddress
        fields = ["address", "currency_code"]
        read_only_fields = ["address"]
