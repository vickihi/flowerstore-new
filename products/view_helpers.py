from django.db.models import Avg, Count, Q

from reviews.models.review import Review
from .models import Product
from .utils import compute_average_rating_stats


def build_related_products(product: Product):
    return Product.objects.filter(category=product.category).exclude(pk=product.id)[:8]


def build_reviews_queryset(product: Product):
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
    base_reviews, reviews = build_reviews_queryset(product)
    average_rating = base_reviews.aggregate(avg=Avg("rating"))["avg"]
    review_count = reviews.count()
    average_rating_value, average_rating_full, average_rating_half = (
        compute_average_rating_stats(average_rating)
    )
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
