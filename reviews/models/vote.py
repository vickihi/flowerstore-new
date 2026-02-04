from django.db import models
from reviews.models.review import Review
from django.core.exceptions import ValidationError

class Vote(models.Model):
    """
    Vote model for a review by a user
    """
    email = models.EmailField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def clean(self):   
        if self.email == self.review.email:
            raise ValidationError("You cannot vote on your own review.")
        
        if Vote.objects.filter(email=self.email, review=self.review).exists():
            raise ValidationError("You have already voted on this review.")
        
