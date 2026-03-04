from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from . import models


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = models.Account
        fields = [
            "full_name",
            "email",
        ]


class AccountProfileForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = [
            "full_name",
            "email",
            "address_line1",
            "address_line2",
            "city",
            "province",
            "postal_code",
            "country",
        ]


class AccountPasswordForm(PasswordChangeForm):
    def clean_new_password1(self):
        """Ensure the new password is not the same as the old password.
        Also the basic password validation inherited from PasswordChangeForm."""
        new_password = self.cleaned_data.get("new_password1")
        if self.user.check_password(new_password):
            raise ValidationError(
                "New password cannot be the same as the old password."
            )
        return new_password
