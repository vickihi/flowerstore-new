from django.db.models import Avg, Q
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404

from reviews.forms import ReviewForm, CommentForm
from .forms import IndexForm, SearchForm, CategoryForm
from .models import Product, Category
from .view_helpers import build_product_detail_context


def index(request):
    index_form = IndexForm(request.GET)
    search_form = SearchForm()
    products = Product.objects.all()

    if not index_form.is_valid():
        return _render_index(request, products, index_form, search_form)

    products = Product.query_with_form(products, index_form.cleaned_data)
    return _render_index(request, products, index_form, search_form)


def _render_index(request, products, index_form, search_form):
    return render(
        request,
        "products/index.html",
        {
            "products": products,
            "index_form": index_form,
            "search_form": search_form,
        },
    )


def search_results(request):
    search_form = SearchForm(request.GET)
    index_form = IndexForm(request.GET)
    products = Product.objects.all()
    search_term = ""

    if not search_form.is_valid():
        return _render_search(request, products, index_form, search_form, search_term)

    search_term = search_form.cleaned_data["search"]
    products = products.search(search_term)

    if index_form.is_valid():
        products = Product.query_with_form(products, index_form.cleaned_data)

    return _render_search(request, products, index_form, search_form, search_term)


def _render_search(request, products, index_form, search_form, search_term):
    return render(
        request,
        "products/search_results.html",
        {
            "products": products,
            "index_form": index_form,
            "search_term": search_term,
            "search_form": search_form,
        },
    )


def apply_sort_and_available(products, form, default_sort):
    sort_order = default_sort

    if form.is_valid():
        sort_order = form.cleaned_data.get("sort_order") or default_sort
        available = form.cleaned_data.get("available")

        if available:
            products = products.available()
    if sort_order in ("rating", "-rating"):
        products = products.annotate(
            avg_rating=Coalesce(
                Avg("reviews__rating", filter=Q(reviews__is_hidden=False)),
                0.0,
            )
        )
        if sort_order == "rating":
            return products.order_by("-avg_rating", "-created_at")
        else:
            return products.order_by("avg_rating", "-created_at")

    return products.order_by(sort_order)


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    cat_form = CategoryForm(request.GET)
    products = apply_sort_and_available(
        products,
        cat_form,
        default_sort="-created_at",
    )

    return render(
        request,
        "products/category.html",
        {
            "category": category,
            "products": products,
            "cat_form": cat_form,
        },
    )


def category_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(
        request,
        "products/categories.html",
        {
            "categories": categories,
            "products": products,
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
