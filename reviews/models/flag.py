from django.core.exceptions import ValidationError
from django.db import models
from reviews.models.review import Review
from django.utils import timezone


class Flag(models.Model):
    """
    Flag model for flag a review.
    """

    FLAG_CHOICES = (
        ("off-topic", "Off-topic"),
        ("inappropriate", "Inappropriate"),
        ("fake", "Fake"),
    )

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="flags")
    email = models.EmailField()
    flag = models.CharField(max_length=20, choices=FLAG_CHOICES)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["review", "email"],
                name="unique_flag_per_review_per_email",
            )
        ]

    def clean(self):
        """
        Ensure that the user cannot flag their own review
        and cannot flag more than once per review.
        """
        if self.review_id and self.email == self.review.email:
            raise ValidationError("You cannot flag your own review.")

        if Flag.objects.filter(email=self.email, review=self.review).exists():
            raise ValidationError("You have already flagged this review.")

    def __str__(self):
        return f"Flag({self.review_id}, {self.email}, {self.flag})"
