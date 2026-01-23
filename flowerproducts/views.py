from django.shortcuts import render, get_object_or_404

from .forms import IndexForm, SearchForm
from .models import Product, Category


def query_products(products, index_form, search_form):
    if index_form.is_valid():
        sort_order = (
            index_form.cleaned_data["sort_order"] or IndexForm.SORT_ORDERS[0][0]
        )
        available = index_form.cleaned_data["available"]
        filter_category = index_form.cleaned_data["filter_category"]

        if sort_order:
            products = products.order_by(sort_order)

        if available:
            products = products.available()

        if filter_category:
            products = products.filter(category=filter_category)

    return products


def index(request):
    index_form = IndexForm(request.GET)
    search_form = SearchForm()
    products = Product.objects.all()

    products = query_products(products, index_form, search_form)

    return render(
        request,
        "flowerproducts/index.html",
        {
            "products": products,
            "index_form": index_form,
            "search_form": SearchForm(),  # empty search
        },
    )


def search_results(request):
    search_form = SearchForm(request.GET)
    index_form = IndexForm(request.GET)
    products = Product.objects.all()

    if search_form.is_valid():
        search_term = search_form.cleaned_data["search"]
        products = query_products(products, index_form, search_form)
        products = products.search(search_term)

    return render(
        request,
        "flowerproducts/search_results.html",
        {
            "products": products,
            "search_form": search_form,
            "index_form": index_form,
            "search_term": search_term,
        },
    )


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    form = IndexForm(request.GET)
    sort_order = IndexForm.SORT_ORDERS[0][0]

    products = Product.objects.filter(category=category)

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
        },
    )


def category_list(request):
    categories = Category.objects.all()
    return render(
        request,
        "flowerproducts/categories.html",
        {"categories": categories},
    )


def product_detail(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
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
