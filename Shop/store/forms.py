from django import forms
from django.forms import ModelForm
from .models import ShippingAddress
from .mixins import FormPlaceholderMixin, FormInputClassMixin


class ShippingForm(FormInputClassMixin, FormPlaceholderMixin, ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = ["customer"]
        labels = {"reciever": "Full name"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
