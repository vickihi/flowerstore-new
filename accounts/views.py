from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from orders.session import CartStore
from . import forms


def register(request):
    """Show form for creating an account."""
    form = forms.AccountCreationForm()
    context = {"form": form}
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
    form = AuthenticationForm()
    context = {"form": form}
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
    return redirect("flowerproducts:index")


@login_required
def profile(request):
    """Show current user profile and order history."""
    profile_form = forms.AccountProfileForm(instance=request.user)
    password_form = forms.AccountPasswordForm(user=request.user)
    user = request.user
    orders = user.orders.filter(payment_id__gt="").order_by("-created_at")
    context = {
        "profile_form": profile_form,
        "password_form": password_form,
        "orders": orders,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def profile_update(request):
    """Handle profile update."""
    profile_form = forms.AccountProfileForm(request.POST, instance=request.user)
    password_form = forms.AccountPasswordForm(user=request.user)
    if not profile_form.is_valid():
        context = {"profile_form": profile_form, "password_form": password_form}
        return render(request, "accounts/profile.html", context)
    profile_form.save()
    return redirect("accounts:profile")


@login_required
def password_update(request):
    """Handle password update."""
    profile_form = forms.AccountProfileForm(instance=request.user)
    password_form = forms.AccountPasswordForm(user=request.user, data=request.POST)
    if not password_form.is_valid():
        context = {"profile_form": profile_form, "password_form": password_form}
        return render(request, "accounts/profile.html", context)
    password_form.save()
    update_session_auth_hash(request, password_form.user)
    return redirect("accounts:profile")
