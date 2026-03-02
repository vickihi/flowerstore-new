from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from orders.session import CartStore

from . import forms


def register(request):
    """Show form for creating an account."""
    context = {"form": forms.AccountCreationForm()}
    return render(request, "accounts/register.html", context)


def register_submit(request):
    """Handle form for creating an account."""
    form = forms.AccountCreationForm(request.POST)
    if not form.is_valid():
        context = {"form": form}
        return render(request, "accounts/register.html", context)
    form.save()
    return redirect("accounts:login")


def login(request):
    """Show form for log in."""
    context = {"form": AuthenticationForm()}
    return render(request, "accounts/login.html", context)


def login_submit(request):
    """Handle form for log in."""
    form = AuthenticationForm(request, request.POST)
    if not form.is_valid():
        context = {"form": form}
        return render(request, "accounts/login.html", context)
    django_login(request, form.get_user())
    cart_store = CartStore(request)
    cart_store.merge_session_cart()
    return redirect("accounts:profile")


def logout(request):
    """Log out the user."""
    django_logout(request)
    return redirect("accounts:login")


@login_required
def profile(request):
    """Show current user profile."""
    return render(request, "accounts/profile.html")
