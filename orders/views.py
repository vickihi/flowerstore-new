from dataclasses import dataclass
from decimal import Decimal


from django.contrib import messages

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render


from flowerproducts.models import Product
from orders.constants import CART_KEY, LEGACY_CART_KEY


@dataclass
class Cart:
    product_id: int
    quantity: int


class CartStore:
    def __init__(self, session) -> None:
        self.session = session
        self.cart: dict[str, int] = session.get(
            CART_KEY, session.get(LEGACY_CART_KEY, {})
        )

    def add(self, product_id: int, quantity: int) -> None:
        p_id = str(product_id)
        quantity = int(quantity)
        if quantity <= 0:
            return
        current_quantity = int(self.cart.get(p_id, 0))
        self.cart[p_id] = current_quantity + quantity
        self._commit()

    def set_quantity(self, product_id: int, quantity: int) -> None:
        p_id = str(product_id)
        quantity = int(quantity)
        if quantity <= 0:
            self.remove_product(product_id)
            return
        self.cart[p_id] = quantity
        self._commit()

    def remove_product(self, product_id: int) -> None:
        p_id = str(product_id)
        if p_id in self.cart:
            del self.cart[p_id]
            self._commit()

    def items(self) -> list[Cart]:
        return [
            Cart(product_id=int(p_id), quantity=int(qty))
            for p_id, qty in self.cart.items()
        ]

    def count_items(self) -> int:
        return sum(int(quantity) for quantity in self.cart.values())

    def as_dict(self) -> dict[str, int]:
        return self.cart

    def _commit(self) -> None:
        self.session[CART_KEY] = self.cart
        self.session.pop(LEGACY_CART_KEY, None)
        self.session.modified = True


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
    cart = CartStore(request.session).as_dict()
    rows = _cart_products(cart)
    order_total = sum((line_total for _, _, line_total in rows), Decimal("0.00"))
    return render(
        request,
        "orders/cart.html",
        {
            "rows": rows,
            "order_total": order_total,
        },
    )
