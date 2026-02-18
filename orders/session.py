from dataclasses import dataclass
from decimal import Decimal

from flowerproducts.models import Product
from orders.constants import CART_KEY


@dataclass
class Cart:
    product_id: int
    quantity: int


class CartStore:
    def __init__(self, session) -> None:
        self.session = session
        self.cart: dict[str, int] = session.get(CART_KEY, {})

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

    def detailed_items(self) -> list[tuple[Product, int, Decimal]]:
        if not self.cart:
            return []
        products = Product.objects.filter(id__in=self.cart.keys())
        rows: list[tuple[Product, int, Decimal]] = []
        for product in products:
            quantity = int(self.cart[str(product.id)])
            line_total = product.price * quantity
            rows.append((product, quantity, line_total))
        return rows

    def _commit(self) -> None:
        self.session[CART_KEY] = self.cart
        self.session.modified = True
