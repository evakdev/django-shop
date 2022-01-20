from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING, SET_NULL
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Sum
from django.db.models import F
from phonenumber_field.modelfields import PhoneNumberField
from cities_light.models import City, Country, Region


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    brand = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    @property
    def main_picture(self):
        main = self.picture_set.filter(is_main=True)
        if main.exists():
            return main.first().image


class Picture(models.Model):
    image = models.ImageField(upload_to="uploads/")
    product = models.ForeignKey(Product, on_delete=CASCADE)
    is_main = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.product.name


class ShippingAddress(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=DO_NOTHING)
    reciever = models.CharField(max_length=150)
    email = models.EmailField()
    phone = PhoneNumberField()
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=DO_NOTHING)
    state = models.ForeignKey(Region, on_delete=DO_NOTHING)
    country = models.ForeignKey(Country, on_delete=DO_NOTHING)
    zip_code = models.CharField(max_length=10)


class Order(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField()
    transaction_id = models.CharField(max_length=100, null=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=SET_NULL, null=True)

    @property
    def is_empty(self):
        return not self.orderitem_set.exists()

    @property
    def total_price(self):
        query = self.orderitem_set.annotate(
            total=F("quantity") * F("product__price")
        ).aggregate(sum=Sum("total"))
        sum = query["sum"]
        if not sum:
            return 0
        return "{:.2f}".format(query["sum"])

    @property
    def total_items(self):
        query = self.orderitem_set.aggregate(sum=Sum("quantity"))
        return query.get("sum")

    def __str__(self) -> str:
        order_items = self.orderitem_set.all().values_list("product__name", flat=True)
        return ", ".join(order_items)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return "{:.2f}".format(self.product.price * self.quantity)

    def __str__(self) -> str:
        return f"{self.product.name} x{self.quantity}"
