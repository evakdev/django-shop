from django import template
from store.models import Order
import json

register = template.Library()


@register.filter
def cart_item_count(request):
    if request.user.is_authenticated:
        query = Order.objects.filter(customer=request.user, completed=False)
        if query.exists():
            order = query.first()
            return order.total_items
    else:
        cart = json.loads(request.COOKIES.get("cart", "{}"))
        item_count = 0
        for key, value in cart.items():
            item_count += value.get("quantity")
        return item_count
