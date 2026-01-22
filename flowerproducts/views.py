from django.shortcuts import render

from .forms import IndexForm
from .models import Product, Category


# Create your views here.
def index(request):
    form = IndexForm(request.GET)

    sort_order = IndexForm.SORT_ORDERS[0][0]
    filter_category = None
    products = Product.objects.all()

    if form.is_valid():
        sort_order = form.cleaned_data.get("sort_order") or sort_order
        filter_category = form.cleaned_data.get("filter_category")

    if filter_category:
        products = products.filter(category_id=filter_category)

    products = products.order_by(sort_order)

    return render(
        request,
        "flowerproducts/index.html",
        {
            "products": products,
            "form": form,
        },
    )


def category_list(request):

    categories = Category.objects.all()
    return render(
        request,
        "flowerproducts/categories.html",
        {"categories": categories},
    )


def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    form = IndexForm(request.GET)
    sort_order = IndexForm.SORT_ORDERS[0][0]

    products = (
        Product.objects
        .filter(category=category)
    )

    if form.is_valid():
        sort_order = form.cleaned_data.get("sort_order") or sort_order

    products = products.order_by(sort_order)

    return render(
        request,
        "flowerproducts/category.html",
        {
            "category": category,
            "products": products,
            "form": form,
        }
    )

def product_detail(request, product_id: int):
    product = Product.objects.get(pk=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(
        pk=product_id
    )[:4]
    return render(
        request,
        "flowerproducts/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
        },
    )
