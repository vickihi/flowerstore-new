
from decimal import Decimal


from django.contrib import messages

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render


from flowerproducts.models import Product

from .forms import CheckoutForm


CART_SESSION_KEY = "shopping_cart"


def _get_cart(request: HttpRequest) -> dict[str, int]:
    return request.session.get(CART_SESSION_KEY, {})


def _save_cart(request: HttpRequest, cart: dict[str, int]) -> None:
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True


def _empty_cart(request: HttpRequest) -> None:
    request.session.pop(CART_SESSION_KEY, None)
    request.session.modified = True


def _cart_products(cart: dict[str, int]) -> list[tuple[Product, int, Decimal]]:
    if not cart:
        return []
    products = Product.objects.filter(id__in=cart.keys())
    rows: list[tuple[Product, int, Decimal]] = []
    for product in products:
        quantity = int(cart[str(product.id)])
        line_total = product.price * quantity
        rows.append((product, quantity, line_total))
    return rows


def add_cart_item(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.method != "POST":
        return redirect("flowerproducts:product_detail", product_id=product_id)

    product = get_object_or_404(Product, id=product_id)
    quantity = max(int(request.POST.get("quantity", 1)), 1)

    cart = _get_cart(request)
    current_quantity = int(cart.get(str(product.id), 0))
    cart[str(product.id)] = current_quantity + quantity
    _save_cart(request, cart)

    messages.success(
        request,
        f"{quantity} item(s) of {product.name} were added to your shopping cart.",
    )
    return redirect("orders:cart_detail")


def update_cart_item(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.method != "POST":
        return redirect("orders:cart_detail")

    cart = _get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    key = str(product.id)
    previous_quantity = int(cart.get(key, 0))

    if previous_quantity == 0:
        messages.error(request, f"{product.name} is not in your shopping cart.")
        return redirect("orders:cart_detail")

    new_quantity = int(request.POST.get("quantity", 0))

    if new_quantity <= 0:
        cart.pop(key, None)
        _save_cart(request, cart)
        messages.success(
            request,
            f"{product.name} was removed from your shopping cart.",
        )
        return redirect("orders:cart_detail")

    cart[key] = new_quantity
    _save_cart(request, cart)
    messages.success(
        request,
        f"The quantity of {product.name} was changed from {previous_quantity} to {new_quantity}.",
    )
    return redirect("orders:cart_detail")


def remove_cart_item(request: HttpRequest, product_id: int) -> HttpResponse:
    if request.method != "POST":
        return redirect("orders:cart_detail")

    cart = _get_cart(request)
    key = str(product_id)
    if key in cart:
        product = get_object_or_404(Product, id=product_id)
        cart.pop(key, None)
        _save_cart(request, cart)
        messages.success(
            request,
            f"{product.name} was removed from your shopping cart.",
        )
    return redirect("orders:cart_detail")


def cart_detail(request: HttpRequest) -> HttpResponse:
    cart = _get_cart(request)
    rows = _cart_products(cart)
    order_total = sum((line_total for _, _, line_total in rows), Decimal("0.00"))
    return render(
        request,
        "orders/cart.html",
        {
            "rows": rows,
            "order_total": order_total,
            "checkout_form": CheckoutForm(),
        },
    )
  
def add_to_cart(request): ...
def checkout_start(request): ...
def checkout_success(request): ...
def checkout_cancel(request): ...
def order_strip_webhook(request): ...

