from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class AccountManager(BaseUserManager):
    def create_user(self, email: str, password: str) -> "Account":
        """Create a user."""
        account = self.model(email=self.normalize_email(email))
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, email: str, password: str) -> "Account":
        """Create a super user."""
        account = self.create_user(email, password)
        account.is_admin = True
        account.is_superuser = True
        account.save()
        return account


class Account(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELD = []

    email = models.EmailField(unique=True)
    password = models.CharField()
    full_name = models.CharField(max_length=120, blank=True, default="")
    address_line1 = models.CharField(max_length=255, blank=True, default="")
    address_line2 = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=120, blank=True, default="")
    province = models.CharField(max_length=120, blank=True, default="")
    postal_code = models.CharField(max_length=20, blank=True, default="")
    country = models.CharField(max_length=2, blank=True, default="CA")
    stripe_customer_id = models.CharField(max_length=100, blank=True, default="")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    def __str__(self):
        """String representation for this account."""
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
