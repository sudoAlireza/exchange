from django.urls import path
from .views import PurchaseOrderView


urlpatterns = [
    path('purchase/', PurchaseOrderView.as_view(), name='purchase-order'),
]
