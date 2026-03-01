from django.contrib.auth.forms import UserCreationForm
from . import models


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = models.Account
        fields = ["email"]
