from decimal import Decimal


from django.contrib import messages

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render


from flowerproducts.models import Product
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
