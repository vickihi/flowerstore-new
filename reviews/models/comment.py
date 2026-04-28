from django.conf import settings
from django.db import models

from reviews.models.review import Review


class Comment(models.Model):
    """Comment on a review."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    body = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user}: {self.body[:25]}..."
