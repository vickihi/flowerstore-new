from django import forms
from .models import Review
from reviews.models.vote import Vote

class BaseEmailForm(forms.Form):
    email = forms.EmailField(label="Email")


class ReviewForm(BaseEmailForm, forms.ModelForm):
    class Meta:
        model = Review
        fields = ["email", "body", "rating"]

# Vote ========================================
class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ["email", "review"]
        widgets = {
            "review": forms.HiddenInput(),
        }

