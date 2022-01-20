from django.contrib import admin
from .models import Product, Picture, ShippingAddress, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    pass


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass
