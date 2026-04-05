from django import forms
from reviews.models.comment import Comment
from reviews.models.flag import Flag
from reviews.models.review import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["body", "rating"]

    def clean_body(self):
        body = self.cleaned_data.get("body", "")
        if not body.strip():
            raise forms.ValidationError("Review cannot be empty.")
        return body

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]

    def clean_body(self):
        body = self.cleaned_data.get("body", "")
        if not body.strip():
            raise forms.ValidationError("Comment cannot be empty.")
        return body

class FlagForm(forms.ModelForm):
    class Meta:
        model = Flag
        fields = ["flag"]
        widgets = {
            "flag": forms.RadioSelect(),
        }
