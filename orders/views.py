import os
from decimal import Decimal, ROUND_HALF_UP

import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from flowerproducts.models import Product
from orders.forms import AddCartItemForm, UpdateCartItemForm
from orders.models import Order, OrderItem, WishlistItem
from orders.session import CartStore


def _build_or_update_stripe_customer(request: HttpRequest) -> str | None:
    """Create or update Stripe customer from authenticated user profile."""
    user = request.user
    if not user.is_authenticated:
        return None

    payload: dict = {"email": user.email}
    if user.full_name:
        payload["name"] = user.full_name

    if user.address_line1:
        payload["address"] = {
            "line1": user.address_line1,
            "line2": user.address_line2 or None,
            "city": user.city or None,
            "state": user.province or None,
            "postal_code": user.postal_code or None,
            "country": user.country or None,
        }

    customer_id = user.stripe_customer_id
    if customer_id:
        try:
            stripe.Customer.modify(customer_id, **payload)
            return customer_id
        except stripe.error.InvalidRequestError:
            customer_id = ""

    customer = stripe.Customer.create(**payload)
    user.stripe_customer_id = customer["id"]
    user.save(update_fields=["stripe_customer_id"])
    return customer["id"]


@require_http_methods(["POST"])
def add_cart_item(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.method != "POST":
        return redirect("flowerproducts:product_detail", product_id=product_id)

    product = get_object_or_404(Product, id=product_id)
    cart_store = CartStore(request)
    form = AddCartItemForm(
        request.POST,
        product=product,
        current_quantity=cart_store.get_quantity(product.id),
    )
    if not form.is_valid():
        error = (
                form.non_field_errors() or form.errors.get("quantity") or ["Invalid input."]
        )
        messages.error(request, str(error[0]))
        return redirect("flowerproducts:product_detail", product_id=product_id)

    requested_quantity = form.cleaned_data["quantity"]
    cart_store.add(product.id, requested_quantity)

    messages.success(
        request,
        f"{requested_quantity} item(s) of {product.name} were added to your shopping cart.",
    )
    return redirect("orders:cart_detail")


@require_http_methods(["POST"])
def update_cart_item(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.method != "POST":
        return redirect("orders:cart_detail")

    cart_store = CartStore(request)
    product = get_object_or_404(Product, id=product_id)
    previous_quantity = cart_store.get_quantity(product.id)

    if previous_quantity == 0:
        messages.error(request, f"{product.name} is not in your shopping cart.")
        return redirect("orders:cart_detail")

    form = UpdateCartItemForm(request.POST, product=product)
    if not form.is_valid():
        error = (
                form.non_field_errors() or form.errors.get("quantity") or ["Invalid input."]
        )
        messages.error(request, str(error[0]))
        return redirect("orders:cart_detail")

    new_quantity = form.cleaned_data["quantity"]
    if new_quantity <= 0:
        cart_store.remove_product(product.id)
        messages.success(
            request,
            f"{product.name} was removed from your shopping cart.",
        )
        return redirect("orders:cart_detail")

    cart_store.set_quantity(product.id, new_quantity)

    messages.success(
        request,
        f"The quantity of {product.name} was changed from {previous_quantity} to {new_quantity}.",
    )
    return redirect("orders:cart_detail")


@require_http_methods(["POST"])
def remove_cart_item(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.method != "POST":
        return redirect("orders:cart_detail")

    cart_store = CartStore(request)
    if cart_store.get_quantity(product_id) > 0:
        product = get_object_or_404(Product, id=product_id)
        cart_store.remove_product(product.id)
        messages.success(
            request,
            f"{product.name} was removed from your shopping cart.",
        )
    return redirect("orders:cart_detail")


def cart_detail(request: HttpRequest) -> HttpResponse:
    cart_store = CartStore(request)
    rows = cart_store.detailed_items()
    order_total = cart_store.order_total(rows)
    return render(
        request,
        "orders/cart.html",
        {
            "rows": rows,
            "order_total": order_total,
        },
    )


@require_http_methods(["POST"])
def checkout(request) -> HttpResponse:
    """Checkout start page"""
    cart_store = CartStore(request)
    rows = cart_store.detailed_items()

    if not rows:
        messages.error(request, "No items were added to your shopping cart.")
        return redirect("orders:cart_detail")

    order = Order()
    if request.user.is_authenticated:
        order.user = request.user
    order.save()
    for product, qty, _line_total in rows:
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty,
            unit_price=product.price,
        )

    stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", None)
    if stripe.api_key is None:
        raise RuntimeError("STRIPE_SECRET_KEY not set.")

    line_items = []
    for product, qty, _line_total in rows:
        unit_amount = int(
            (product.price * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        )

        line_items.append(
            {
                "price_data": {
                    "currency": "cad",
                    "unit_amount": unit_amount,
                    "product_data": {
                        "name": product.name,
                    },
                },
                "quantity": qty,
            }
        )

    checkout_kwargs = {
        "client_reference_id": str(order.id),
        "line_items": line_items,
        "mode": "payment",
        "billing_address_collection": "required",
        "shipping_address_collection": {"allowed_countries": ["CA", "US"]},
        "success_url": request.build_absolute_uri(reverse("orders:checkout_success")),
    }
    if request.user.is_authenticated:
        customer_id = _build_or_update_stripe_customer(request)
        if customer_id:
            checkout_kwargs["customer"] = customer_id

    checkout_session = stripe.checkout.Session.create(**checkout_kwargs)
    request.session["last_order_id"] = order.id
    return redirect(checkout_session.url, code=303)


def checkout_success(request: HttpRequest) -> HttpResponse:
    order_id = request.session.get("last_order_id")
    order = Order.objects.filter(pk=order_id).first() if order_id else None
    if not order or not order.is_fulfilled:
        messages.info(
            request, "Payment is still processing. Please check again shortly."
        )
        return redirect("orders:cart_detail")

    cart_store = CartStore(request)
    cart_store.clear()
    request.session.pop("last_order_id", None)
    return render(request, "orders/success.html")


@login_required
def wishlist_detail(request: HttpRequest) -> HttpResponse:
    items = (WishlistItem.objects.
             filter(user=request.user).
             select_related("product")
             )
    return (render
            (request, "orders/wishlist.html",
             {"items": items})
            )


@login_required
@require_http_methods(["POST"])
def wishlist_add(request: HttpRequest, product_id) -> HttpResponse:
    product = get_object_or_404(Product, id=product_id)
    item, created = WishlistItem.objects.get_or_create(
        user=request.user,
        product=product,
    )
    if created:
        messages.success(request, f"{product.name} was added to your wish list.")
    else:
        messages.info(request, f"{product.name} is already in your wish list.")
    return redirect("flowerproducts:product_detail", product_id=product_id)


@login_required
@require_http_methods(["POST"])
def wishlist_remove(request: HttpRequest, product_id) -> HttpResponse:
    product = get_object_or_404(Product, id=product_id)
    item = WishlistItem.objects.filter(user=request.user, product=product).first()

    if item:
        item.delete()
        messages.success(request, f"{product.name} was removed from your wish list.")
    else:
        messages.info(request, f"{product.name} is not in your wish list.")

    return redirect("orders:wishlist_detail")


@login_required
@require_http_methods(["POST"])
def wishlist_move_to_cart(request: HttpRequest, product_id) -> HttpResponse:
    product = get_object_or_404(Product, id=product_id)
    item = WishlistItem.objects.filter(user=request.user, product=product).first()
    if not item:
        messages.info(request, f"{product.name} is not in wish list.")
        return redirect("orders:wishlist_detail")

    cart_store = CartStore(request)
    cart_store.add(product.id, 1)
    item.delete()

    messages.success(request, f"{product.name} was moved to your Cart.")
    return redirect("orders:cart_detail")
