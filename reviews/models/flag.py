from django.core.exceptions import ValidationError
from django.db import models
from reviews.models.review import Review
from django.utils import timezone
from django.conf import settings


class Flag(models.Model):
    """
    Flag model for flag a review.
    """

    FLAG_CHOICES = (
        ("off-topic", "Off-topic"),
        ("inappropriate", "Inappropriate"),
        ("fake", "Fake"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="flags",
        null=True, blank=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="flags")
    email = models.EmailField()
    flag = models.CharField(max_length=20, choices=FLAG_CHOICES)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["review", "user"],
                name="unique_flag_per_review_per_user",
            )
        ]

    def clean(self):
        """
        Ensure that the user cannot flag their own review
        and cannot flag more than once per review.
        """
        if self.review_id and self.user_id == self.review.user_id:
            raise ValidationError("You cannot flag your own review.")

        if Flag.objects.filter(user=self.user, review=self.review).exists():
            raise ValidationError("You have already flagged this review.")

    def __str__(self):
        return f"Flag({self.review_id}, {self.user}, {self.flag})"
