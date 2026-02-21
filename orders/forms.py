from django import forms


class BaseCartItemForm(forms.Form):
    quantity = forms.IntegerField(required=False)
    default_quantity = 0
    min_quantity = 0

    def __init__(self, *args, product, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product
        self.fields["quantity"].min_value = self.min_quantity

    def quantity_for_stock_check(self, quantity: int) -> int:
        return quantity

    def clean_quantity(self) -> int:
        quantity = self.cleaned_data.get("quantity")
        if quantity is None:
            quantity = self.default_quantity
        quantity = int(quantity)

        if self.quantity_for_stock_check(quantity) > self.product.quantity:
            raise forms.ValidationError(
                f"Only {self.product.quantity} item(s) of {self.product.name} are in stock."
            )
        return quantity


class AddCartItemForm(BaseCartItemForm):
    default_quantity = 1
    min_quantity = 1

    def __init__(self, *args, product, current_quantity=0, **kwargs):
        super().__init__(*args, product=product, **kwargs)
        self.current_quantity = int(current_quantity)

    def quantity_for_stock_check(self, quantity: int) -> int:
        return self.current_quantity + quantity


class UpdateCartItemForm(BaseCartItemForm):
    default_quantity = 0
    min_quantity = 0
