from decimal import Decimal

from django.conf import settings
from django.db import models


class Order(models.Model):
    """Order model for orders."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, blank=True, default="")
    customer_name = models.CharField(max_length=100, blank=True, default="")
    customer_email = models.EmailField(blank=True, default="")
    bill_address = models.TextField(blank=True, default="")
    ship_address = models.TextField(blank=True, default="")

    @property
    def total_price(self) -> Decimal:
        return sum(
            (item.unit_price * item.quantity for item in self.items.all()),
            Decimal("0.00"),
        )

    @property
    def is_fulfilled(self) -> bool:
        """Return True if order is fulfilled."""
        return self.payment_id != ""

    def fulfill(
            self,
            name: str,
            email: str,
            payment_id: str,
            billing_address: dict = None,
            shipping_address: dict = None,
    ) -> None:
        """Fulfill this order."""
        self.customer_name = name
        self.customer_email = email
        self.payment_id = payment_id
        self.bill_address = billing_address
        self.ship_address = shipping_address or self.bill_address
        self.save()


class OrderItem(models.Model):
    """OrderItem model for order items."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("flowerproducts.Product", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"],
                name="unique_order_item",
            )
        ]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class CartItem(models.Model):
    """Persistent cart row for authenticated users."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    product = models.ForeignKey("flowerproducts.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_cart_item",
            )
        ]

    def __str__(self):
        return f"{self.user_id}:{self.product_id} x {self.quantity}"


class WishlistItem(models.Model):
    """WishlistItem model for authenticated users."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
    )

    product = models.ForeignKey("flowerproducts.Product", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_wishlist_item",
            )
        ]

    def __str__(self):
        return f"{self.user_id}:{self.product_id}"
