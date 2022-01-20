from django.http.response import HttpResponseRedirect
from store.models import Order, OrderItem
from store.mixins import CookieCartMixin
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls.base import reverse_lazy
from .forms import (
    SignupForm,
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    EditProfileForm,
)
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView
import json
from django.db.models import F


class SignupView(SuccessMessageMixin, CreateView):
    form_class = SignupForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("login")
    success_message = "Your profile was created successfully"


from django.core.serializers import serialize
from django.forms.models import model_to_dict


class LoginView(CookieCartMixin, LoginView):
    form_class = CustomAuthenticationForm
    template_name = "account/login.html"

    def form_valid(self, form):
        user = form.get_user()
        self.update_cart(user)
        response = super().form_valid(form)

        response.delete_cookie('cart')
        return response

    def update_cart(self, user):
        cookie_cart = json.loads(self.request.COOKIES.get("cart", "{}"))
        order, order_created = Order.objects.get_or_create(
            customer=user, completed=False
        )

        for product, data in cookie_cart.items():
            item, item_created = OrderItem.objects.get_or_create(
                order=order, product_id=product
            )
            quantity = data.get("quantity")
            item.quantity = F("quantity") + quantity - (1 if item_created else 0)
            item.save()


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "account/profile.html"

    def get_object(self, queryset=None):
        return self.request.user


from django.forms.models import model_to_dict


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = "account/profile_change_form.html"
    form_class = EditProfileForm
    success_url = reverse_lazy("profile")

    def get_initial(self):
        user = self.request.user
        return model_to_dict(user)

    def get_object(self):
        return self.request.user


class LogoutView(LogoutView):
    template_name = "account/logged_out.html"


class PasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "account/password_change_form.html"


class PasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "account/password_change_done.html"


class PasswordResetView(PasswordResetView):
    template_name = "account/password_reset_form.html"
    form_class = CustomPasswordResetForm


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "account/password_reset_done.html"


class PasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = "account/password_reset_confirm.html"


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"
