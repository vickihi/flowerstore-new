from django import forms
from reviews.models.review import Review
from reviews.models.vote import Vote
from reviews.models.comment import Comment


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
        fields = ["email"]


# Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["email", "body"]
