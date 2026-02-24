from django.db import models
from flowerproducts.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator


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
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        help_text="Rating score given by the user (1–5).",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the review was created."
    )

    is_hidden = models.BooleanField(
        default=False, help_text="Whether this review is hidden due to moderation."
    )

    @property
    def flag_count(self)-> int:
        """Returns the number of flags for this review."""
        return self.flags.count()

    def update_hidden_status(self):
        """Updates the hidden status of the review based on flag count."""
        if self.flag_count > 5:
            self.is_hidden = True
            self.save(update_fields=["is_hidden"])

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "email"],
                name="unique_review_per_product_per_email",
            )
        ]

    @property
    def vote_count(self) -> int:
        return self.vote_set.count()

    def __str__(self):
        return f"Review({self.product}, {self.email}, rating={self.rating})"
