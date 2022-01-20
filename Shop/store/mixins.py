import json
from django.forms.widgets import Select

from django.shortcuts import get_object_or_404
from .models import Product


class FormPlaceholderMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_names = [field_name for field_name, _ in self.fields.items()]
        for field_name in field_names:
            field = self.fields.get(field_name)
            field.widget.attrs.update({"placeholder": field.label})


class FormInputClassMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_names = [field_name for field_name, _ in self.fields.items()]
        for field_name in field_names:
            field = self.fields.get(field_name)
            classes = f"{'form-select' if isinstance(field.widget, Select) else 'form-control'} mb-2 border"
            field.empty_label = field_name if isinstance(field.widget, Select) else None
            field.widget.attrs.update({"class": classes})


class CookieCartMixin:
    def get_cookie_cart_context(self, request):
        cookie_cart = json.loads(request.COOKIES.get("cart", "{}"))
        items = []
        total = 0
        for key, value in cookie_cart.items():
            product = get_object_or_404(Product, id=int(key))
            quantity = value.get("quantity")
            item = {
                "product": {
                    "id": key,
                    "name": product.name,
                    "price": product.price,
                    "main_picture": {"url": product.main_picture.url},
                },
                "quantity": quantity,
                "total_price": quantity * product.price,
            }
            items.append(item)
            total += quantity * product.price
        context = {
            "is_empty": not (bool(total)),
            "items": items,
            "total": total,
        }
        return context
