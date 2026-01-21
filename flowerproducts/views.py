from django.shortcuts import render
from .models import Product
from .forms import IndexForm


def index(request):
    form = IndexForm(request.GET)
    if not form.is_valid():
        form = IndexForm()

    default_sort_order = IndexForm.SORT_ORDERS[0][0]
    sort_order = form.cleaned_data["sort_order"] or default_sort_order
    products = Product.objects.order_by(sort_order)

    context = {
        "products": products,
        "form": form,
    }

    return render(request, "products/home.html", context)
