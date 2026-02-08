from django.core.exceptions import ValidationError
from django.db import models
from reviews.models.review import Review


class Flag(models.Model):
    """
    Flag model for flag a review.
    """

    OFF_TOPIC = "off-topic"
    INAPPROPRIATE = "inappropriate"
    FAKE = "fake"

    FLAG_CHOICES = (
        (OFF_TOPIC, "Off-topic"),
        (INAPPROPRIATE, "Inappropriate"),
        (FAKE, "Fake"),
    )

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="flags")
    email = models.EmailField()
    flag = models.CharField(max_length=20, choices=FLAG_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["review", "email"],
                name="unique_flag_per_review_per_email",
            )
        ]

    def clean(self):
        """Ensure that the user cannot flag their own review."""
        if not self.review_id:
            return
        if self.email == self.review.email:
            raise ValidationError("You cannot flag your own review.")
        if Flag.objects.filter(review=self.review, email=self.email).exists():
            raise ValidationError("You have already voted on this review.")

    def __str__(self):
        return f"Flag({self.review_id}, {self.email}, {self.flag})"
