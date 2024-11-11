from rest_framework.routers import DefaultRouter
from wallet.views import WalletAddressViewSet, WalletDepositWithdrawViewSet

router = DefaultRouter()
router.register(r"", WalletDepositWithdrawViewSet, basename="wallet")
router.register(r"addresses", WalletAddressViewSet, basename="address")

urlpatterns = router.urls
