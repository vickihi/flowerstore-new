from django.db.models import Avg, Count, Q
from reviews.models.review import Review
from .models import Product
from .utils import compute_average_rating_stats


def filter_products(products, cleaned_data, *, default_sort="-created_at"):
    """Filter and sort a product queryset from form cleaned_data.
    
    Pass an empty dict when the form is invalid to fall back to default_sort.
    filter_category is only present in ProductFilterForm (index/search views).
    """
    sort_order = cleaned_data.get("sort_order") or default_sort
    available = cleaned_data.get("available")
    filter_category = cleaned_data.get("filter_category")

    if available:
        products = products.available()

    if filter_category:
        products = products.filter(category=filter_category)

    if sort_order in ("avg_rating", "-avg_rating"):
        products = products.with_avg_rating()
        return products.order_by(sort_order, "-created_at")

    return products.order_by(sort_order)


def build_related_products(product: Product):
    """Return up to 8 products in the same category, excluding the given product."""
    return Product.objects.filter(category=product.category).exclude(pk=product.id)[:8]


def build_reviews_queryset(product: Product):
    """Return (base_reviews, annotated_reviews) for a product.
    base_reviews: unhidden reviews, used for aggregate calculations.
    annotated_reviews: includes vote/flag counts, ordered by helpfulness.
    """
    base_reviews = Review.objects.filter(product=product, is_hidden=False)
    reviews = base_reviews.annotate(
        vote_total=Count("votes", distinct=True),
        flag_total=Count("flags", distinct=True),
        flag_off_topic=Count("flags", filter=Q(flags__flag="off-topic"), distinct=True),
        flag_inappropriate=Count(
            "flags", filter=Q(flags__flag="inappropriate"), distinct=True
        ),
        flag_fake=Count("flags", filter=Q(flags__flag="fake"), distinct=True),
    ).order_by(
        "-vote_total",
        "-created_at",
    )
    return base_reviews, reviews


def build_reviews_context(product: Product):
    """Return a context dict with reviews and rating stats for a product."""
    base_reviews, reviews = build_reviews_queryset(product)
    average_rating = base_reviews.aggregate(avg=Avg("rating"))["avg"]
    review_count = reviews.count()
    _, average_rating_full, average_rating_half = compute_average_rating_stats(average_rating)
    return {
        "reviews": reviews,
        "average_rating": average_rating,
        "average_rating_full": average_rating_full,
        "average_rating_half": average_rating_half,
        "review_count": review_count,
        "star_range": range(1, 6),
    }


def build_product_detail_context(
    *,
    product: Product,
    review_form,
    comment_form,
):
    related_products = build_related_products(product)
    reviews_context = build_reviews_context(product)

    return {
        "product": product,
        "related_products": related_products,
        **reviews_context,
        "review_form": review_form,
        "comment_form": comment_form,
    }
