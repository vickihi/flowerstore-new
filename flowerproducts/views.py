from django.shortcuts import render, get_object_or_404, redirect
from .forms import IndexForm, SearchForm, CategoryForm, AddToCartForm, ReviewForm
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
