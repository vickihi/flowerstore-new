from django.contrib.auth.forms import UserCreationForm
from . import models


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = models.Account
        fields = [
            "email",
            "full_name",
            "address_line1",
            "address_line2",
            "city",
            "province",
            "postal_code",
            "country",
        ]
