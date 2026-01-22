from django import forms


class IndexForm(forms.Form):
    SORT_ORDERS = [
        ("-created_at", "Date (newest to oldest)"),
        ("created_at", "Date (oldest to newest)"),
        ("views_count", "Most popular")
    ]

    sort_order = forms.ChoiceField(
        label="Order by", required=False, choices=SORT_ORDERS,
    )

    available = forms.BooleanField(
        required=False,
        label="Show only available products",
    )
