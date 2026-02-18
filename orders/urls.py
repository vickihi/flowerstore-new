from django.urls import path
from . import views


app_name = "orders"
urlpatterns = [
    path("orders/checkout", views.checkout_start, name="checkout_start"),
    path("success/", views.checkout_success, name="checkout_success"),
]
