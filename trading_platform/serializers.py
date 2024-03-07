from rest_framework import serializers

from trading_platform.models import Product, NetworkNode


class ProductSerializer(serializers.ModelSerializer):
    """
    Product Serializer

    This serializer is used to serialize and deserialize Product objects.
    """
    class Meta:
        model = Product
        fields = ('id', 'name', 'model', 'release_date', 'created_at')
        read_only_fields = ('id', 'created_at')


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    This class defines the Serializer for the NetworkNode model.

    The Serializer is used to serialize and deserialize NetworkNode objects.
    """

    products = ProductSerializer(many=True, read_only=True)
    """
    This field defines a many-to-many relationship between the NetworkNode model and the Product model.
    The field returns a list of products associated with the node, and it is read-only.
    """

    product_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Product.objects.all(),
        source='products'
    )
    """
    This field defines a many-to-many relationship between the NetworkNode model and the Product model.
    The field allows the user to specify a list of product IDs to be associated with the node.
    The field is write-only, and it is validated against the Product model.
    """

    supplier = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(),
        allow_null=True,
        required=False
    )
    """
    This field defines a one-to-many relationship between the NetworkNode model and the NetworkNode model.
    The field allows the user to specify a supplier node, and it is validated against the NetworkNode model.
    The field is nullable.
    """

    supplier_name = serializers.StringRelatedField(source='supplier.name', read_only=True)
    """
    This field defines a many-to-one relationship between the NetworkNode model and the NetworkNode model.
    The field returns the name of the supplier node, and it is read-only.
    The field is derived from the 'supplier' field using the 'source' parameter.
    """

    class Meta:
        model = NetworkNode
        fields = [
            'id',
            'name',
            'email',
            'city',
            'street',
            'house_number',
            'node_type',
            'supplier',
            'supplier_name',
            'products',
            'product_ids',
            'debt',
            'created_at',
            'level'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'products',
            'level',
            'supplier_name'
        ]

    def validate(self, data):
        """
        This method is used to validate the input data.

        The method checks the 'node_type' field and the 'supplier' field, and raises a ValidationError if the input data is invalid.
        The method sets the 'level' field based on the 'node_type' and 'supplier' fields.
        """
        node_type = data.get('node_type')
        supplier = data.get('supplier')

        if node_type == 'Factory':
            if supplier is not None:
                raise serializers.ValidationError("The factory cannot have a supplier")
            data['level'] = 0
        elif node_type!= 'Factory':
            if supplier is None:
                raise serializers.ValidationError("Non-factory nodes must have a supplier")
            if supplier.level >= 2:
                raise serializers.ValidationError("The hierarchy level cannot be more than 2")
            data['level'] = supplier.level + 1

        return data

    def create(self, validated_data):
        """
        This method is used to create a new NetworkNode object.

        The method populates the 'products' field based on the 'product_ids' field, and then creates a new NetworkNode object using the validated data.
        The method adds the products to the new node, and returns the new node.
        """
        product_ids = validated_data.pop('products', [])
        network_node = NetworkNode.objects.create(**validated_data)
        for product in product_ids:
            network_node.products.add(product)
        return network_node

    def update(self, instance, validated_data):
        """
        This method is used to update an existing NetworkNode object.

        The method populates the 'products' field based on the 'product_ids' field, and then updates the existing NetworkNode object using the validated data.
        The method sets the 'products' field to the specified products, and then returns the updated node.
        """
        product_ids = validated_data.get('product_ids')
        validated_data.pop('debt', None)
        if product_ids is not None:
            instance.products.set(product_ids)
        return super().update(instance, validated_data)
