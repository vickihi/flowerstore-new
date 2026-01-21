from django.shortcuts import render
from .models import Product, Category


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()

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
        "categories": categories,
        "current_sort": sort,
    }

    return render(request, "products/home.html", context)


