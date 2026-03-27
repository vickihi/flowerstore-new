from django import forms

from reviews.models.comment import Comment
from reviews.models.flag import Flag
from reviews.models.review import Review
from reviews.models.vote import Vote


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["body", "rating"]


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = []


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]


class FlagForm(forms.ModelForm):
    class Meta:
        model = Flag
        fields = ["flag"]
        widgets = {
            "flag": forms.RadioSelect(),
        }
