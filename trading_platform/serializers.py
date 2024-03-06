from rest_framework import serializers

from trading_platform.models import Product, NetworkNode


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'model', 'release_date', 'created_at')
        read_only_fields = ('id', 'created_at')


# class NetworkNodeSerializer(serializers.ModelSerializer):
#     products = ProductSerializer(many=True, read_only=True)
#     product_ids = serializers.PrimaryKeyRelatedField(
#         many=True,
#         write_only=True,
#         queryset=Product.objects.all(),
#         source='products'
#     )
#     supplier = serializers.StringRelatedField(source='supplier.name')
#
#     class Meta:
#         model = NetworkNode
#         fields = ['id', 'name', 'email', 'city', 'street', 'house_number', 'node_type', 'supplier', 'products',
#                   'product_ids', 'debt', 'created_at', 'level']
#         read_only_fields = ['id', 'created_at', 'products', 'level']
#
#     def validate(self, data):
#         node_type = data.get('node_type')
#         supplier = data.get('supplier')
#         print(supplier)
#         if node_type == 'Factory':
#             if supplier is not None:
#                 raise serializers.ValidationError("The factory cannot have a supplier")
#             data['level'] = 0
#         elif node_type != 'Factory' and supplier is None:
#             raise serializers.ValidationError("Non-factory nodes must have a supplier")
#         else:
#             if supplier.level >= 2:
#                 raise serializers.ValidationError("The hierarchy level cannot be more than 2")
#             data['level'] = supplier.level + 1
#
#         return data
#
#     def create(self, validated_data):
#         products = validated_data.pop('products', [])
#         network_node = NetworkNode.objects.create(**validated_data)
#         for product in products:
#             network_node.products.add(product)
#         return network_node
#
#     def update(self, instance, validated_data):
#         product_ids = validated_data.get('product_ids')
#         validated_data.pop('debt')
#         if product_ids is not None:
#             instance.products.set(product_ids)
#         return super().update(instance, validated_data)
class NetworkNodeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Product.objects.all(),
        source='products'
    )
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(),
        allow_null=True,
        required=False
    )
    supplier_name = serializers.StringRelatedField(source='supplier.name', read_only=True)

    class Meta:
        model = NetworkNode
        fields = ['id', 'name', 'email', 'city', 'street', 'house_number', 'node_type', 'supplier', 'supplier_name',
                  'products', 'product_ids', 'debt', 'created_at', 'level']
        read_only_fields = ['id', 'created_at', 'products', 'level', 'supplier_name']

    def validate(self, data):
        node_type = data.get('node_type')
        supplier = data.get('supplier')

        if node_type == 'Factory':
            if supplier is not None:
                raise serializers.ValidationError("The factory cannot have a supplier")
            data['level'] = 0
        elif node_type != 'Factory':
            if supplier is None:
                raise serializers.ValidationError("Non-factory nodes must have a supplier")
            if supplier.level >= 2:
                raise serializers.ValidationError("The hierarchy level cannot be more than 2")
            data['level'] = supplier.level + 1

        return data

    def create(self, validated_data):
        product_ids = validated_data.pop('products', [])
        network_node = NetworkNode.objects.create(**validated_data)
        for product in product_ids:
            network_node.products.add(product)
        return network_node

    def update(self, instance, validated_data):
        product_ids = validated_data.get('product_ids')
        validated_data.pop('debt', None)
        if product_ids is not None:
            instance.products.set(product_ids)
        return super().update(instance, validated_data)
