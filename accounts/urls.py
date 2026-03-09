from django.urls import reverse_lazy
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("register/submit/", views.register_submit, name="register_submit"),
    path("login/", views.login, name="login"),
    path("login/submit/", views.login_submit, name="login_submit"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/update/", views.profile_update, name="profile_update"),
    path(
        "profile/password/update/",
        views.password_update,
        name="profile_password_update",
    ),
    path(
        "password-reset/",
        CustomPasswordResetView.as_view(
            template_name="accounts/password_reset_form.html",
            email_template_name="accounts/password_reset_email.html",
            success_url="/accounts/password-reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
