from dataclasses import dataclass

CART_KEY = "cart"


@dataclass
class Cart:
    product_id: int
    quantity: int


class CartStore:
    def __init__(self, session):
        self.session = session
        self.cart: dict[str, int] = session.get(CART_KEY, {})

    def add(self, product_id: int, quantity) -> None:
        """Add a product to the cart"""
        p_id = str(product_id)
        quantity = int(quantity)

        if quantity <= 0:
            return

        current_quantity = int(self.cart.get(p_id, 0))
        self.cart[p_id] = current_quantity + quantity
        self._commit()

    def set_quantity(self, product_id: int, quantity: int) -> None:
        """Add a product to the cart"""
        p_id = str(product_id)
        quantity = int(quantity)

        if quantity <= 0:
            return

        self.cart[p_id] = quantity
        self._commit()

    def remove_product(self, product_id: int) -> None:
        """Remove a product from the cart"""
        p_id = str(product_id)
        if p_id in self.cart:
            del self.cart[p_id]
            self._commit()

    def items(self) -> list[Cart]:
        """Return all products in the cart"""

    def count_items(self) -> int:
        """Return the number of products in the cart"""

    def _commit(self) -> None:
        self.session.modified = True
