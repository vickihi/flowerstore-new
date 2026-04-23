from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from reviews.models.review import Review


class Vote(models.Model):
    """Vote on a review."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="votes")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "review"],
                name="unique_vote_per_user_per_review",
            )
        ]

    def clean(self):
        if self.user_id == self.review.user_id:
            raise ValidationError("You cannot vote on your own review.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Vote by {self.user} on review #{self.review.id}"
