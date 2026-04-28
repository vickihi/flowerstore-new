from django.conf import settings
from django.db import models

from reviews.models.review import Review


class Flag(models.Model):
    """Flag a review."""

    FLAG_CHOICES = (
        ("off-topic", "Off-topic"),
        ("inappropriate", "Inappropriate"),
        ("fake", "Fake"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="flags")
    flag = models.CharField(max_length=20, choices=FLAG_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["review", "user"],
                name="unique_flag_per_review_per_user",
            )
        ]

    def __str__(self):
        return f"Flag({self.review_id}, {self.user}, {self.flag})"
