from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import viewsets,filters,generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Category,Product,Cart,CartItem,Order,OrderItem,ShippingAddress
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategorySerializer,ProductSerializer,CartSerializer,CartItemSerializer,OrderSerializer,OrderItemSerializer,ShippingAddressSerializer,RegisterSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class CategoryView(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    
class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']  # Filter by ?category=1
    search_fields = ['name', 'description']  # Search by name or description
    
class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]  # import from rest_framework.permissions

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_or_create_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

class CartItemView(viewsets.ModelViewSet):
    queryset=CartItem.objects.all()
    serializer_class=CartItemSerializer
    permission_classes=[IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cart_id']
    
    # def get_queryset(self):
    #     cart=Cart.objects.filter(user=self.request.user)
    #     queryset=CartItem.objects.filter(cart=cart)
    #     return queryset
    
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
    
    def perform_create(self, serializer):
        cart = serializer.validated_data['cart']
        if cart.user != self.request.user:
            raise PermissionDenied("You cannot add items to someone else's cart.")
        serializer.save()

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderItemView(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order']  # filter order items by order id

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)

from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(user=user, total_amount=total_amount, status=Order.Status.PENDING)

    # Create OrderItems
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        product=item.product
        product.stock=product.stock-item.quantity
        product.save()

    # Clear the cart after ordering
    cart_items.delete()

    from .serializers import OrderSerializer
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ShippingAddressView(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)