from rest_framework import viewsets

from trading_platform.models import Product, NetworkNode
from trading_platform.permissions import IsActive
from trading_platform.serializers import ProductSerializer, NetworkNodeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActive]


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows network nodes to be viewed or edited.

        Methods
        -------
        list:
            Returns a list of all network nodes.
        retrieve:
            Returns the details of a specific network node.
        create:
            Creates a new network node.
        update:
            Updates an existing network node.
        partial_update:
            Partially updates an existing network node.
        destroy:
            Deletes an existing network node.

        Permissions
        -----------
        IsActive:
            Only active network nodes can be accessed or modified.

        Attributes
        -----------
        queryset:
            The queryset of all network nodes.
        serializer_class:
            The serializer class used for validating and deserializing input and output data.
        permission_classes:
            A list of permission classes that determine the user's access rights.
    """
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActive]
