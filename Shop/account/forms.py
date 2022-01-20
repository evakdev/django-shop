from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.forms.models import ModelForm

from store.mixins import FormInputClassMixin, FormPlaceholderMixin


class SignupForm(FormInputClassMixin, FormPlaceholderMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "gender",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gender"].empty_label = "Gender"


class EditProfileForm(FormInputClassMixin, FormPlaceholderMixin, ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "first_name", "last_name", "gender"]


class CustomAuthenticationForm(
    FormInputClassMixin, FormPlaceholderMixin, AuthenticationForm
):
    pass


class CustomPasswordChangeForm(
    FormInputClassMixin, FormPlaceholderMixin, PasswordChangeForm
):
    pass


class CustomPasswordResetForm(
    FormInputClassMixin, FormPlaceholderMixin, PasswordResetForm
):
    pass


class CustomSetPasswordForm(FormInputClassMixin, FormPlaceholderMixin, SetPasswordForm):
    pass
