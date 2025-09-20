from rest_framework import serializers
from .models import User, Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock',
        ]

    def validate_price(self, value):
        if not value>0:
            raise serializers.ValidationError('Price must not be negative.') 
        return value
    
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.price')
    class Meta:
        model = OrderItem
        fields = [
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal',
        ]
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    class Meta:
        model = Order
        fields = [
            'order_id',
            'user', 
            'created_at', 
            'status',
            'items',
            'total_price',
        ]
