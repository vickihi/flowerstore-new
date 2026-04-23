from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from orders.session import CartStore
from . import forms


def register(request):
    """Show form for creating an account."""
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    form = forms.AccountCreationForm()
    context = {"form": form}
    return render(request, "accounts/register.html", context)


@require_POST
def register_submit(request):
    """Handle form for creating an account."""
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    form = forms.AccountCreationForm(request.POST)
    if not form.is_valid():
        context = {"form": form}
        return render(request, "accounts/register.html", context)
    form.save()
    request.session["prefill_email"] = form.cleaned_data["email"]
    return redirect("accounts:login")


def login(request):
    """Show form for log in."""
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    initial_email = request.session.pop("prefill_email", "")
    form = AuthenticationForm(initial={"username": initial_email})
    context = {"form": form}
    return render(request, "accounts/login.html", context)


@require_POST
def login_submit(request):
    """Handle form for log in."""
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    form = AuthenticationForm(request, request.POST)
    if not form.is_valid():
        context = {"form": form}
        return render(request, "accounts/login.html", context)
    django_login(request, form.get_user())
    cart_store = CartStore(request)
    cart_store.merge_session_cart()
    next_url = request.POST.get("next") or request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("accounts:profile")


@require_POST
def logout(request):
    """Log out the user."""
    django_logout(request)
    return redirect("products:index")


@login_required
def profile(request):
    """Show current user profile and order history."""
    profile_form = forms.AccountProfileForm(instance=request.user)
    password_form = forms.AccountPasswordForm(user=request.user)
    user = request.user
    orders = user.orders.exclude(payment_id="").order_by("-created_at")
    context = {
        "profile_form": profile_form,
        "password_form": password_form,
        "orders": orders,
    }
    return render(request, "accounts/profile.html", context)


@login_required
@require_POST
def profile_update(request):
    """Handle profile update."""
    profile_form = forms.AccountProfileForm(request.POST, instance=request.user)
    password_form = forms.AccountPasswordForm(user=request.user)
    if not profile_form.is_valid():
        context = {"profile_form": profile_form, "password_form": password_form}
        return render(request, "accounts/profile.html", context)
    profile_form.save()
    messages.success(request, "Your profile has been updated successfully.")
    return redirect("accounts:profile")


@login_required
@require_POST
def password_update(request):
    """Handle password update."""
    profile_form = forms.AccountProfileForm(instance=request.user)
    password_form = forms.AccountPasswordForm(user=request.user, data=request.POST)
    if not password_form.is_valid():
        context = {"profile_form": profile_form, "password_form": password_form}
        return render(request, "accounts/profile.html", context)
    password_form.save()
    update_session_auth_hash(request, password_form.user)
    messages.success(request, "Your password has been updated successfully.")
    return redirect("accounts:profile")


class CustomPasswordResetView(PasswordResetView):
    """Handle password reset.
    Save the email for prefilling the form after password reset."""
    def form_valid(self, form):
        self.request.session["prefill_email"] = form.cleaned_data["email"]
        return super().form_valid(form)
