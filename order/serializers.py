from rest_framework import serializers

from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class PurchaseOrderSerializer(serializers.Serializer):
    currency_code = serializers.CharField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
