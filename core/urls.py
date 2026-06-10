# shop/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryView, ProductView, CartView, CartItemView,
    OrderView, OrderItemView, ShippingAddressView
)
from .views import RegisterView,get_or_create_cart,place_order
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('categories', CategoryView, basename='category')
router.register('products', ProductView, basename='product')
router.register('carts', CartView, basename='cart')
router.register('cart-items', CartItemView, basename='cartitem')
router.register('orders', OrderView, basename='order')
router.register('order-items', OrderItemView, basename='orderitem')
router.register('shipping-addresses', ShippingAddressView, basename='shippingaddress')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-cart/', get_or_create_cart,name='user-cart'),
    path('place-order/', place_order, name='place-order'),
]

