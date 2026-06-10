from django.contrib import admin
from .models import Category,Cart,CartItem,Order,OrderItem,ShippingAddress,Product

# Register your models here.

admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)