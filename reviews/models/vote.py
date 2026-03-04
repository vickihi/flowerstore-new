from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from reviews.models.review import Review


class Vote(models.Model):
    """
    Vote model for vote a review.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="votes", null=True, blank=True)
    email = models.EmailField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "review")

    def clean(self):
        """
        Ensure a user cannot vote on their own review
        and cannot vote more than once per review.
        """
        if self.review_id is None:
            return

        if self.user_id == self.review.user_id:
            raise ValidationError("You cannot vote on your own review.")

        if Vote.objects.filter(user=self.user, review=self.review).exists():
            raise ValidationError("You have already voted on this review.")

    def __str__(self):
        return f"Vote by {self.user} on review #{self.review.id}"
