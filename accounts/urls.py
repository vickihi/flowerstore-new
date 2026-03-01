from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("register/submit/", views.register_submit, name="register_submit"),
    path("login/", views.login, name="login"),
    path("login/submit/", views.login_submit, name="login_submit"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
]