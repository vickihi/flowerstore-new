from django import forms


class IndexForm(forms.Form):
    SORT_ORDERS = [
        ("price", "Price (low to high)"),
        ("-price", "Price (high to low)"),
        ("popular", "Most popular"),
    ]
    sort_order = forms.ChoiceField(
        label="Order by", required=False, choises=SORT_ORDERS
    )
    

    available = forms.BooleanField(
        required=False,
        label="Only available",
    )

