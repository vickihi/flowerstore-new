from django import forms
from .models import Category

class IndexForm(forms.Form):
    SORT_ORDERS = [
        ("-created_at", "Date (newest to oldest)"),
        ("created_at", "Date (oldest to newest)"),
    ]

    sort_order = forms.ChoiceField(
        label="Order by", required=False, choices=SORT_ORDERS
    )
    

    available = forms.BooleanField(
        required=False,
    )

    filter_category = forms.ModelChoiceField(
        label="Category",
        required=False,
        queryset=Category.objects.all(),
    )