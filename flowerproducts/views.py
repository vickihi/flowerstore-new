from django.shortcuts import render, get_object_or_404, redirect

from .forms import IndexForm, SearchForm, CategoryForm, AddToCartForm, ReviewForm
from .models import Product, Category


def query_products(products, index_form):
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

    products = query_products(products, index_form)

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

    if search_form.is_valid():
        search_term = search_form.cleaned_data["search"]
        products = query_products(products, index_form)
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
    )[:4]
    return render(
        request,
        "flowerproducts/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
            "cart_form": AddToCartForm(),
            "review_form": ReviewForm(),
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


def add_review(request, product_id):
    if request.method != "POST":
        return redirect("flowerproducts:product_detail", product_id)

    form = ReviewForm(request.POST)
    if form.is_valid():
        # content = form.cleaned_data["content"]
        # TODO: add review
        pass

    return redirect("flowerproducts:product_detail", product_id)
