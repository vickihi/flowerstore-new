from django.db import models
from flowerproducts.models import Product


class Review(models.Model):
    """
    Core review entity.
    Represents a user's review of a product.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    email = models.EmailField(help_text="Email address of the review author.")

    body = models.TextField(help_text="Review content written by the user.")

    rating = models.PositiveSmallIntegerField(
        help_text="Rating score given by the user (1–5)."
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the review was created."
    )

    is_hidden = models.BooleanField(
        default=False, help_text="Whether this review is hidden due to moderation."
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "email"],
                name="unique_review_per_product_per_email",
            )
        ]

    def __str__(self):
        return f"Review({self.product}, {self.email}, rating={self.rating})"
