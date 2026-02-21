from django.urls import path

from . import views, webhooks

app_name = "orders"

urlpatterns = [
    path("cart/", views.cart_detail, name="cart_detail"),
    path(
        "cart/add/<int:product_id>/",
        views.add_cart_item,
        name="add_cart_item",
    ),
    path(
        "cart/update/<int:product_id>/",
        views.update_cart_item,
        name="update_cart_item",
    ),
    path(
        "cart/remove/<int:product_id>/",
        views.remove_cart_item,
        name="remove_cart_item",
    ),
    path("checkout/start", views.checkout_start, name="checkout_start"),
    path("success/", views.checkout_success, name="checkout_success"),
    path(
        "webhook/",
        webhooks.stripe_webhook,
        name="fulfill_stripe_checkout_webhook",
    ),
]
