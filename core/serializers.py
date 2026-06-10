from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, Cart, CartItem, Order, OrderItem, ShippingAddress

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'created_at', 'updated_at']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'product_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_amount', 'ordered_at']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']

class ShippingAddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShippingAddress
        fields = ['user', 'address', 'city', 'state', 'zipcode', 'country']
        read_only_fields=["user"]