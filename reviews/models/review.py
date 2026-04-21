from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from products.models import Product

FLAG_HIDE_THRESHOLD = 5


class Review(models.Model):
    """
    Core review entity.
    Represents a user's review of a product.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    body = models.TextField(max_length=2000)
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        help_text="Rating score given by the user (1-5).",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(
        default=False, help_text="Whether this review is hidden due to moderation."
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "user"],
                name="unique_review_per_product_per_user",
            )
        ]

    def __str__(self):
        return f"Review({self.product}, {self.user}, rating={self.rating})"

    @property
    def flag_count(self) -> int:
        """Returns the number of flags for this review."""
        return self.flags.count()

    def update_hidden_status(self):
        """Updates the hidden status of the review based on flag count."""
        if self.flag_count > FLAG_HIDE_THRESHOLD:
            self.is_hidden = True
            self.save(update_fields=["is_hidden"])
