from rest_framework import viewsets

from trading_platform.models import Product, NetworkNode
from trading_platform.permissions import IsActive
from trading_platform.serializers import ProductSerializer, NetworkNodeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActive]


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActive]
