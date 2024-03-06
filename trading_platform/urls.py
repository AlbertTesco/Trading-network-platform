from django.urls import path, include
from rest_framework.routers import DefaultRouter

from trading_platform.apiviews import ProductViewSet, NetworkNodeViewSet
from trading_platform.apps import TradingPlatformConfig

app_name = TradingPlatformConfig.name

router = DefaultRouter()

router.register(r'products', ProductViewSet)
router.register(r'network-node', NetworkNodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
