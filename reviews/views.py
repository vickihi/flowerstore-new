from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product
from products.view_helpers import build_product_detail_context
# from orders.models import OrderItem
from reviews.models.review import Review
from reviews.models.vote import Vote
from .forms import ReviewForm, CommentForm, FlagForm


@require_POST
@login_required
def add_review(request, product_id):
    """ Add a review to a product. """
    product = get_object_or_404(Product, pk=product_id)

    # Temporary comment out for testing
    # has_purchased = (
    #     OrderItem.objects.filter(
    #         product=product,
    #         order__user=request.user,
    #     )
    #     .exclude(order__payment_id="")
    #     .exists()
    # )
    # if not has_purchased:
    #     messages.error(request, "You can only review the product you have purchased.")
    #     return redirect("products:product_detail", product.id)

    review_form = ReviewForm(request.POST)
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.product = product
        review.user = request.user
        try:
            review.save()
            return redirect("products:product_detail", product_id=product_id)
        except IntegrityError:
            review_form.add_error(None, "You have already reviewed this product.")

    return render(
        request,
        "products/product_detail.html",
        build_product_detail_context(
            product=product,
            review_form=review_form,
            comment_form=CommentForm(),
        ),
    )


@require_POST
@login_required
def add_vote(request, review_id):
    """ Add a vote to a review. """
    review = get_object_or_404(Review, pk=review_id)

    if review.user_id == request.user.id:
        messages.error(request, "You cannot vote on your own review.")
        return redirect("products:product_detail", product_id=review.product.id)

    vote = Vote(review=review, user=request.user)
    try:
        vote.save()
    except IntegrityError:
        messages.error(request, "You have already voted on this review.")

    return redirect("products:product_detail", product_id=review.product.id)


@require_POST
@login_required
def add_comment(request, review_id):
    """ Add a comment to a review. """
    review = get_object_or_404(Review, pk=review_id)

    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()

    return redirect("products:product_detail", product_id=review.product.id)


@require_POST
@login_required
def add_flag(request, review_id):
    """ Add a flag to a review. """
    review = get_object_or_404(Review, pk=review_id)

    if review.user_id == request.user.id:
        messages.error(request, "You cannot flag your own review.")
        return redirect("products:product_detail", product_id=review.product.id)

    flag_form = FlagForm(request.POST)
    if flag_form.is_valid():
        flag = flag_form.save(commit=False)
        flag.review = review
        flag.user = request.user
        try:
            flag.save()
        except IntegrityError:
            messages.error(request, "You have already flagged this review.")

    return redirect("products:product_detail", product_id=review.product.id)
    # Review needs render because it has complex form error
    # Comment/Vote/Flag has no complex form error render like Review, so directly redirect product detail page
