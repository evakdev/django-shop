import json
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from .models import OrderItem, Product, Order
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import F
from .forms import ShippingForm
from .mixins import CookieCartMixin


class StoreView(ListView):
    model = Product
    paginate_by = 10
    template_name = "store/store.html"


class CartView(CookieCartMixin, View):
    def get(self, request):
        customer = request.user
        if customer.is_authenticated:
            order, created = Order.objects.get_or_create(customer_id=customer.id)
            context = {
                "is_empty": order.is_empty,
                "items": order.orderitem_set.all(),
                "total": order.total_price,
            }
        else:
            context = self.get_cookie_cart_context(request)
        return render(request, "store/cart.html", context)


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        self.user = request.user
        self.check_cart_content()
        context = self.get_context()
        initial_form_input = {"name": self.user.full_name, "email": self.user.email}
        context["form"] = ShippingForm(initial=initial_form_input)

        return render(request, "store/checkout.html", context=context)

    def post(self, request):
        self.user = request.user
        form = ShippingForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.customer = request.user
            shipping_address.save()
            order = get_object_or_404(Order, customer_id=self.user.id, completed=False)
            order.shipping_address = shipping_address
            order.save()
            return HttpResponse({"suceess": "sds"})
        else:
            context = self.get_context()
            context["form"] = form
            return render(request, "store/checkout.html", context=context)

    def get_context(self):
        order = get_object_or_404(Order, customer_id=self.user.id, completed=False)
        context = {
            "items": order.orderitem_set.all(),
            "total": order.total_price,
        }
        return context

    def check_cart_content(self):
        query = Order.objects.filter(customer_id=self.user.id, completed=False)
        if query.exists():
            order = query.first()
            if not order.orderitem_set.exists():
                return redirect("cart")
        else:
            return redirect("cart")


class UpdateUserCartView(View):
    def post(self, request):
        data = json.loads(request.body)
        id, action = int(data.get("id")), data.get("action")
        product = get_object_or_404(Product, id=id)
        order, order_created = Order.objects.get_or_create(
            customer=request.user.id, completed=False
        )
        order_item, item_created = OrderItem.objects.get_or_create(
            order=order, product=product
        )
        if action == "add" and not item_created:

            order_item.quantity = F("quantity") + 1
            order_item.save()

        elif action == "remove":
            if order_item.quantity <= 1:
                order_item.delete()
            else:
                order_item.quantity = F("quantity") - 1
                order_item.save()

        return JsonResponse({"add": "done"})
