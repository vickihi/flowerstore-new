from dataclasses import dataclass
from decimal import Decimal

from products.models import Product
from orders.constants import CART_KEY
from orders.models import CartItem


@dataclass
class Cart:
    product_id: int
    quantity: int


class CartStore:
    def __init__(self, request) -> None:
        self.request = request
        self.session = request.session
        self.user = request.user
        self.cart: dict[str, int] = self.session.get(CART_KEY, {})

    @property
    def is_authenticated(self) -> bool:
        return self.user.is_authenticated

    def add(self, product_id: int, quantity: int) -> None:
        """Add a product to the cart."""
        quantity = int(quantity)
        if quantity <= 0:
            return
        if self.is_authenticated:
            cart_item, _created = CartItem.objects.get_or_create(
                user=self.user,
                product_id=product_id,
                defaults={"quantity": 0},
            )
            cart_item.quantity += quantity
            cart_item.save(update_fields=["quantity"])
            return

        p_id = str(product_id)
        current_quantity = int(self.cart.get(p_id, 0))
        self.cart[p_id] = current_quantity + quantity
        self._commit()

    def set_quantity(self, product_id: int, quantity: int) -> None:
        """Set product quantity in the cart."""
        quantity = int(quantity)
        if quantity <= 0:
            self.remove_product(product_id)
            return
        if self.is_authenticated:
            CartItem.objects.update_or_create(
                user=self.user,
                product_id=product_id,
                defaults={"quantity": quantity},
            )
            return

        p_id = str(product_id)
        self.cart[p_id] = quantity
        self._commit()

    def remove_product(self, product_id: int) -> None:
        """Remove a product from the cart."""
        if self.is_authenticated:
            CartItem.objects.filter(user=self.user, product_id=product_id).delete()
            return

        p_id = str(product_id)
        if p_id in self.cart:
            del self.cart[p_id]
            self._commit()

    def get_quantity(self, product_id: int) -> int:
        """Return quantity for one product in cart, or 0 if absent."""
        if self.is_authenticated:
            quantity = (
                CartItem.objects.filter(user=self.user, product_id=product_id)
                .values_list("quantity", flat=True)
                .first()
            )
            return int(quantity or 0)

        return int(self.cart.get(str(product_id), 0))

    def items(self) -> list[Cart]:
        """Return all products in the cart."""
        if self.is_authenticated:
            return [
                Cart(product_id=item.product_id, quantity=item.quantity)
                for item in CartItem.objects.filter(user=self.user)
            ]

        return [
            Cart(product_id=int(p_id), quantity=int(qty))
            for p_id, qty in self.cart.items()
        ]

    def count_items(self) -> int:
        """Return total quantity of products in the cart."""
        if self.is_authenticated:
            return sum(
                int(quantity)
                for quantity in CartItem.objects.filter(user=self.user).values_list(
                    "quantity", flat=True
                )
            )

        return sum(int(quantity) for quantity in self.cart.values())

    def detailed_items(self) -> list[tuple[Product, int, Decimal]]:
        """Return cart rows as (product, quantity, line_total)."""
        if self.is_authenticated:
            rows: list[tuple[Product, int, Decimal]] = []
            for item in CartItem.objects.filter(user=self.user).select_related(
                "product"
            ):
                product = item.product
                quantity = int(item.quantity)
                line_total = product.price * quantity
                rows.append((product, quantity, line_total))
            return rows

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

    def clear(self) -> None:
        """Clear all items in the current cart."""
        if self.is_authenticated:
            CartItem.objects.filter(user=self.user).delete()
            return
        self.cart = {}
        if CART_KEY in self.session:
            del self.session[CART_KEY]
            self.session.modified = True

    def merge_session_cart(self) -> None:
        """Merge session cart into DB cart and clear session cart."""
        if not self.is_authenticated:
            return

        session_cart = self.session.get(CART_KEY, {})
        if not session_cart:
            return

        valid_ids = [int(pid) for pid in session_cart.keys() if str(pid).isdigit()]
        products = Product.objects.in_bulk(valid_ids)
        for raw_pid, raw_qty in session_cart.items():
            if not str(raw_pid).isdigit():
                continue

            product_id = int(raw_pid)
            if product_id not in products:
                continue

            quantity = int(raw_qty)
            if quantity <= 0:
                continue
            self.add(product_id, quantity)

        del self.session[CART_KEY]
        self.session.modified = True
