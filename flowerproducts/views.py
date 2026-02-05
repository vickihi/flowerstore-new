from django.db.models import Avg, Count
from django.shortcuts import render, get_object_or_404, redirect
from .forms import IndexForm, SearchForm, CategoryForm, AddToCartForm
from reviews.forms import ReviewForm, CommentForm
from reviews.models.review import Review
from .models import Product, Category


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
        "flowerproducts/index.html",
        {
            "products": products,
            "index_form": index_form,
            "search_form": search_form,  # empty search
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
        "flowerproducts/search_results.html",
        {
            "products": products,
            "index_form": index_form,
            "search_term": search_term,
            "search_form": search_form,
        },
    )


def apply_sort_and_available(products, form, default_sort):
    if form.is_valid():
        sort_order = form.cleaned_data.get("sort_order") or default_sort
        available = form.cleaned_data.get("available")

        if sort_order:
            products = products.order_by(sort_order)

        if available:
            products = products.available()

    return products


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
        "flowerproducts/category.html",
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
        "flowerproducts/categories.html",
        {
            "categories": categories,
            "products": products,
        },
    )


def product_detail(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(
        pk=product_id
    )[:3]
    base_reviews = Review.objects.filter(product=product, is_hidden=False)
    average_rating = base_reviews.aggregate(avg=Avg("rating"))["avg"]
    reviews = base_reviews.annotate(vote_count=Count("vote")).order_by(
        "-vote_count",
        "-created_at",
    )
    review_count = reviews.count()
    average_rating_value = float(average_rating or 0)
    average_rating_rounded = round(average_rating_value * 2) / 2
    average_rating_full = int(average_rating_rounded)
    average_rating_half = (average_rating_rounded - average_rating_full) == 0.5
    return render(
        request,
        "flowerproducts/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
            "reviews": reviews,
            "average_rating": average_rating,
            "average_rating_full": average_rating_full,
            "average_rating_half": average_rating_half,
            "review_count": review_count,
            "star_range": range(1, 6),
            "cart_form": AddToCartForm(),
            "review_form": ReviewForm(),
            "comment_form": CommentForm(),
        },
    )


def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("flowerproducts:product_detail", product_id)

    form = AddToCartForm(request.POST)
    if form.is_valid():
        # quantity = form.cleaned_data["quantity"]
        # TODO: add to cart
        pass

    return redirect("flowerproducts:product_detail", product_id)
