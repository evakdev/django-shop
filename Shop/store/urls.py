from django.urls import path
from .views import StoreView, CartView, CheckoutView, UpdateUserCartView

urlpatterns = [
    path("", StoreView.as_view(), name="home"),
    path("cart/", CartView.as_view(), name="cart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("update_user_cart/", UpdateUserCartView.as_view(), name="update_user_cart"),
]
