from django import forms


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(max_length=255)
    customer_email = forms.EmailField()
