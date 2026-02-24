from django.db import models
from reviews.models.review import Review
from django.core.exceptions import ValidationError


class Vote(models.Model):
    """
    Vote model for vote a review.
    """

    email = models.EmailField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("email", "review")

    def clean(self):
        """
        Ensure a user cannot vote on their own review
        and cannot vote more than once per review.
        """
        if self.review_id is None:
            return

        if self.email == self.review.email:
            raise ValidationError("You cannot vote on your own review.")

        if Vote.objects.filter(email=self.email, review=self.review).exists():
            raise ValidationError("You have already voted on this review.")

    def __str__(self):
        return f"Vote by {self.email} on review #{self.review.id}"
