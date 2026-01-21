from django import forms


class IndexForm(forms.Form):
    SORT_CHOICES = [
        ("popular", "Most popular"),
    ]

    available = forms.BooleanField(
        required=False,
        label="Only available",
    )

