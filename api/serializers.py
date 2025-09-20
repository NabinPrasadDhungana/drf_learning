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