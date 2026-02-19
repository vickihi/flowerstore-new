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
        """Add a product to the cart."""
        p_id = str(product_id)
        quantity = int(quantity)
        if quantity <= 0:
            return
        current_quantity = int(self.cart.get(p_id, 0))
        self.cart[p_id] = current_quantity + quantity
        self._commit()

    def add_with_stock_limit(
        self, product_id: int, quantity: int, max_quantity: int
    ) -> bool:
        """Add quantity only if final cart quantity does not exceed stock."""
        p_id = str(product_id)
        quantity = int(quantity)
        max_quantity = max(int(max_quantity), 0)
        if quantity <= 0:
            return False
        current_quantity = int(self.cart.get(p_id, 0))
        final_quantity = current_quantity + quantity
        if final_quantity > max_quantity:
            return False
        self.cart[p_id] = final_quantity
        self._commit()
        return True

    def set_quantity(self, product_id: int, quantity: int) -> None:
        """Set product quantity in the cart."""
        p_id = str(product_id)
        quantity = int(quantity)
        if quantity <= 0:
            self.remove_product(product_id)
            return
        self.cart[p_id] = quantity
        self._commit()

    def set_quantity_with_stock_limit(
        self, product_id: int, quantity: int, max_quantity: int
    ) -> bool:
        """Set quantity only if requested quantity does not exceed stock."""
        quantity = int(quantity)
        max_quantity = max(int(max_quantity), 0)
        if quantity <= 0:
            self.remove_product(product_id)
            return True
        if quantity > max_quantity:
            return False
        self.set_quantity(product_id, quantity)
        return True

    def remove_product(self, product_id: int) -> None:
        """Remove a product from the cart."""
        p_id = str(product_id)
        if p_id in self.cart:
            del self.cart[p_id]
            self._commit()

    def get_quantity(self, product_id: int) -> int:
        """Return quantity for one product in cart, or 0 if absent."""
        return int(self.cart.get(str(product_id), 0))

    def items(self) -> list[Cart]:
        """Return all products in the cart."""
        return [
            Cart(product_id=int(p_id), quantity=int(qty))
            for p_id, qty in self.cart.items()
        ]

    def count_items(self) -> int:
        """Return total quantity of products in the cart."""
        return sum(int(quantity) for quantity in self.cart.values())

    def as_dict(self) -> dict[str, int]:
        """Expose the raw cart mapping (product_id -> quantity)."""
        return self.cart

    def detailed_items(self) -> list[tuple[Product, int, Decimal]]:
        """Return cart rows as (product, quantity, line_total)."""
        if not self.cart:
            return []
        ids_in_cart: list[int] = [int(pid) for pid in self.cart.keys()]
        products = Product.objects.in_bulk(ids_in_cart)  # {id: Product}
        rows: list[tuple[Product, int, Decimal]] = []
        for pid in ids_in_cart:
            product = products.get(pid)
            if product is None:
                continue
            quantity = int(self.cart[str(pid)])
            line_total = product.price * quantity
            rows.append((product, quantity, line_total))
        return rows

    def order_total(
        self, rows: list[tuple[Product, int, Decimal]] | None = None
    ) -> Decimal:
        """Return order total from rows, or from current cart when rows are omitted."""
        cart_rows = rows if rows is not None else self.detailed_items()
        return sum((line_total for _, _, line_total in cart_rows), Decimal("0.00"))

    def _commit(self) -> None:
        """Persist in-memory cart changes back to the session."""
        self.session[CART_KEY] = self.cart
        self.session.modified = True
