from django import forms
from .models import Category


SORT_ORDERS = [
    ("name", "Name (A to Z)"),
    ("-name", "Name (Z to A)"),
    ("price", "Price (low to high)"),
    ("-price", "Price (high to low)"),
    ("-created_at", "Date (newest to oldest)"),
    ("created_at", "Date (oldest to newest)"),
    ("-avg_rating", "Rating (high to low)"),
    ("avg_rating", "Rating (low to high)"),
]
SORT_CHOICES = [("", ""), *SORT_ORDERS]


class FilterForm(forms.Form):
    sort_order = forms.ChoiceField(
        label="Order by",
        required=False,
        choices=SORT_CHOICES,
    )

    available = forms.BooleanField(
        required=False,
        label="Show only available products",
    )

    # Only rendered in index/search views; ignored in category views
    filter_category = forms.ModelChoiceField(
        label="Category",
        required=False,
        queryset=Category.objects.all(),
    )


class SearchForm(forms.Form):
    search = forms.CharField(
        label="Search",
        required=False,
    )
