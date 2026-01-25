from django import forms
from .models import Category


class IndexForm(forms.Form):
    SORT_ORDERS = [
        ("name", "Name (A to Z)"),
        ("-name", "Name (Z to A)"),
        ("price", "Price (low to high)"),
        ("-price", "Price (high to low)"),
        ("-created_at", "Date (newest to oldest)"),
        ("created_at", "Date (oldest to newest)"),
        ("views_count", "Most popular"),
    ]

    sort_order = forms.ChoiceField(
        label="Order by",
        required=False,
        choices=SORT_ORDERS,
    )

    available = forms.BooleanField(
        required=False,
        label="Show only available products",
    )

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


class ProductDetailForm(forms.Form):
    quantity = forms.IntegerField(
        label="Quantity",
        min_value=1,
        required=False,
    )

    note = forms.CharField(
        label="Note",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )

class CategoryForm(forms.Form):
    SORT_ORDERS = [
        ("name", "Name (A to Z)"),
        ("-name", "Name (Z to A)"),
        ("price", "Price (low to high)"),
        ("-price", "Price (high to low)"),
        ("-created_at", "Date (newest to oldest)"),
        ("created_at", "Date (oldest to newest)"),
        ("views_count", "Most popular"),
    ]

    sort_order = forms.ChoiceField(
        label="Order by",
        required=False,
        choices=SORT_ORDERS,
    )

    available = forms.BooleanField(
        required=False,
        label="Show only available products",
    )
