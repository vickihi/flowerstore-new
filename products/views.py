from django.shortcuts import render, get_object_or_404

from reviews.forms import ReviewForm, CommentForm
from .forms import FilterForm, SearchForm, SORT_ORDERS
from .models import Product, Category
from .view_helpers import build_product_detail_context, filter_products


def index(request):
    filter_form = FilterForm(request.GET)
    search_form = SearchForm(request.GET)
    products = Product.objects.all()
    search_term = ""

    if search_form.is_valid():
        search_term = search_form.cleaned_data["search"]
        if search_term:
            products = products.search(search_term)

    if filter_form.is_valid():
        products = filter_products(products, filter_form.cleaned_data)

    return render(
        request,
        "products/index.html",
        {
            "products": products,
            "filter_form": filter_form,
            "search_form": search_form,
            "search_term": search_term,
            "active_filters": _get_active_filters(filter_form),
        },
    )


def _get_active_filters(form):
    """Returns a dict of active filter chips."""
    if not form.is_valid():
        return {}
    data = form.cleaned_data
    active = {}
    if data.get("filter_category"):
        active["category"] = str(data["filter_category"])
    if data.get("sort_order"):
        active["sort"] = dict(SORT_ORDERS).get(data["sort_order"], data["sort_order"])
    if data.get("available"):
        active["available"] = True
    return active


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    filter_form = FilterForm(request.GET)

    if filter_form.is_valid():
        products = filter_products(products, filter_form.cleaned_data)

    return render(
        request,
        "products/category.html",
        {
            "category": category,
            "products": products,
            "filter_form": filter_form,
        },
    )


def category_list(request):
    categories = Category.objects.all()
    selected_id = request.GET.get("category")
    filter_form = FilterForm(request.GET)

    selected_category = (
        Category.objects.filter(id=selected_id).first() if selected_id else None
    )
    products = (
        Product.objects.filter(category=selected_category)
        if selected_category
        else Product.objects.all()
    )
    if filter_form.is_valid():
        products = filter_products(products, filter_form.cleaned_data)

    return render(
        request,
        "products/categories.html",
        {
            "categories": categories,
            "products": products,
            "selected_category": selected_category,
            "filter_form": filter_form,
        },
    )


def product_detail(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    return render(
        request,
        "products/product_detail.html",
        build_product_detail_context(
            product=product,
            review_form=ReviewForm(),
            comment_form=CommentForm(),
        ),
    )
