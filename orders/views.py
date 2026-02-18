import os
from decimal import Decimal, ROUND_HALF_UP

import stripe
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from flowerproducts.models import Product
from orders.models import Order, OrderItem
from orders.session import CartStore


def add_cart_item(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.method != "POST":
        return redirect("flowerproducts:product_detail", product_id=product_id)

    product = get_object_or_404(Product, id=product_id)
    quantity = max(int(request.POST.get("quantity", 1)), 1)

    cart_store = CartStore(request.session)
    cart_store.add(product.id, quantity)

    messages.success(
        request,
        f"{quantity} item(s) of {product.name} were added to your shopping cart.",
    )
    return redirect("orders:cart_detail")


def update_cart_item(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.method != "POST":
        return redirect("orders:cart_detail")

    cart_store = CartStore(request.session)
    cart = cart_store.as_dict()
    product = get_object_or_404(Product, id=product_id)
    key = str(product.id)
    previous_quantity = int(cart.get(key, 0))

    if previous_quantity == 0:
        messages.error(request, f"{product.name} is not in your shopping cart.")
        return redirect("orders:cart_detail")

    new_quantity = int(request.POST.get("quantity", 0))

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


def remove_cart_item(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.method != "POST":
        return redirect("orders:cart_detail")

    cart_store = CartStore(request.session)
    cart = cart_store.as_dict()
    key = str(product_id)
    if key in cart:
        product = get_object_or_404(Product, id=product_id)
        cart_store.remove_product(product.id)
        messages.success(
            request,
            f"{product.name} was removed from your shopping cart.",
        )
    return redirect("orders:cart_detail")


def cart_detail(request: HttpRequest) -> HttpResponse:
    cart_store = CartStore(request.session)
    rows = cart_store.detailed_items()
    order_total = sum((line_total for _, _, line_total in rows), Decimal("0.00"))
    return render(
        request,
        "orders/cart.html",
        {
            "rows": rows,
            "order_total": order_total,
        },
    )


def checkout_start(request) -> HttpResponse:
    """Checkout start page"""
    if request.method != "POST":
        return redirect("orders:cart_detail")
    cart_store = CartStore(request.session)
    rows = cart_store.detailed_items()

    if not rows:
        messages.error(request, "No items were added to your shopping cart.")
        return redirect("orders:cart_detail")

    order = Order()
    order.save()
    order_total = Decimal("0.00")

    for product, qty, line_total in rows:
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty,
            unit_price=product.price,
        )
        order_total += line_total

    order.total_price = order_total
    order.save(update_fields=["total_price"])

    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

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
                        # "images": [ urls... ]
                    },
                },
                "quantity": qty,
            }
        )

    checkout_session = stripe.checkout.Session.create(
        client_reference_id=str(order.id),
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(reverse("orders:checkout_success")),
        cancel_url=request.build_absolute_uri(reverse("orders:checkout_cancel")),
    )

    return redirect(checkout_session.url, code=303)


def checkout_success(request): ...


def checkout_cancel(request): ...


def order_strip_webhook(request): ...
