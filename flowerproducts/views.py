from django.shortcuts import render
from .models import Product
from .forms import IndexForm


def index(request):
    form = IndexForm(request.GET)
    if not form.is_valid():
        form = IndexForm()

    # Sorting
    SORT_MAP = {
        "price_asc": "price",
        "price_desc": "-price",
        "popular": "-views_count",
    }

    sort = request.GET.get("sort")
    if sort in SORT_MAP:
        products = products.order_by(SORT_MAP[sort])

    context = {
        "products": products,
        "form": form,
    }

    return render(request, "products/home.html", context)


