from django.db import models
from reviews.models.review import Review
from django.conf import settings

class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments", null=True, blank=True)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255, blank=True, default="")
    email = models.EmailField()

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.author}: {self.body[:25]}..."
