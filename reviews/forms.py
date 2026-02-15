from django import forms

from reviews.models.comment import Comment
from reviews.models.flag import Flag
from reviews.models.review import Review
from reviews.models.vote import Vote


class BaseEmailForm(forms.Form):
    email = forms.EmailField(label="Email")


class ReviewForm(BaseEmailForm, forms.ModelForm):
    class Meta:
        model = Review
        fields = ["email", "body", "rating"]


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ["email"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["email", "body"]


class FlagForm(forms.ModelForm):
    class Meta:
        model = Flag
        fields = ["email", "flag"]
        widgets = {
            "flag": forms.RadioSelect(),
        }
