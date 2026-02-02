from django import forms
from .models import Review


class BaseEmailForm(forms.Form):
    email = forms.EmailField(label="Email")


class ReviewForm(BaseEmailForm, forms.ModelForm):
    class Meta:
        model = Review
        fields = ["email", "body", "rating"]
