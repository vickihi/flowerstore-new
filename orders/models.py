from django.db import models


class Order(models.Model):
    """Order model for orders."""

    created_at = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, blank=True, default="")
    customer_name = models.CharField(max_length=100, blank=True, default="")
    customer_email = models.EmailField(blank=True, default="")
    bill_address = models.TextField(blank=True, default="")
    ship_address = models.TextField(blank=True, default="")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def is_fulfilled(self) -> bool:
        """Return True if order is fulfilled."""
        return bool(self.payment_id)  # fix

    def fulfill(
        self,
        name: str,
        email: str,
        payment_id: str,
        billing_address: str = "",
        shipping_address: str = "",
    ) -> None:
        """Fulfill this order."""
        self.customer_name = name
        self.customer_email = email
        self.payment_id = payment_id
        self.bill_address = billing_address
        self.ship_address = shipping_address
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
