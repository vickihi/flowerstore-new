from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from flowerproducts.models import Product
from flowerproducts.view_helpers import build_product_detail_context
from reviews.models.flag import Flag
from reviews.models.review import Review
from reviews.models.vote import Vote
from .forms import ReviewForm, VoteForm, CommentForm, FlagForm


@require_POST
@login_required
def add_review(request, product_id):
    """Handle form to add review to a product."""
    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.email = request.user.email
        try:
            review.save()
            return redirect("flowerproducts:product_detail", product_id=product_id)
        except IntegrityError:
            form.add_error(None, "You have already reviewed this product.")

    return render(
        request,
        "flowerproducts/product_detail.html",
        build_product_detail_context(
            product=product,
            review_form=form,
            comment_form=CommentForm(),
        ),
    )


@login_required
def create_vote(request, review_id):
    """Show form to create a vote."""
    review = get_object_or_404(Review, pk=review_id)
    form = VoteForm()
    context = {"form": form, "review": review}
    return render(request, "reviews/create_vote.html", context)


@require_POST
@login_required
def create_vote_submit(request, review_id):
    """Handle form to submit a vote."""
    review = get_object_or_404(Review, pk=review_id)

    if review.user_id == request.user.id:
        messages.error(request, "You cannot vote on your own review.")
        return redirect("flowerproducts:product_detail", review.product.id)

    vote = Vote(review=review)
    form = VoteForm(request.POST, instance=vote)

    if not form.is_valid():
        context = {"form": form, "review": review}
        return render(request, "reviews/create_vote.html", context)

    vote.user = request.user
    vote.email = request.user.email
    try:
        vote.save()
    except IntegrityError:
        messages.error(request, "You have already voted this review.")
    return redirect("flowerproducts:product_detail", review.product.id)


@require_POST
@login_required
def add_comment(request, review_id):
    """Add comment to review."""
    review = get_object_or_404(Review, pk=review_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.email = request.user.email
        comment.author = request.user.full_name or request.user.email
        comment.save()
    else:
        messages.error(request, "There was an error with your comment.")
    return redirect("flowerproducts:product_detail", review.product.id)


@login_required
def create_flag(request, review_id):
    """Show form to create a flag."""
    review = get_object_or_404(Review, pk=review_id)
    form = FlagForm()
    context = {"form": form, "review": review}
    return render(request, "reviews/create_flag.html", context)


@require_POST
@login_required
def create_flag_submit(request, review_id):
    """Handle form to submit a flag."""
    review = get_object_or_404(Review, pk=review_id)

    if review.user_id == request.user.id:
        messages.error(request, "You cannot flag your own review.")
        return redirect("flowerproducts:product_detail", review.product.id)

    flag = Flag(review=review)
    form = FlagForm(request.POST, instance=flag)

    if not form.is_valid():
        context = {"form": form, "review": review}
        return render(request, "reviews/create_flag.html", context)

    flag.user = request.user
    flag.email = request.user.email
    try:
        flag.save()
    except IntegrityError:
        messages.error(request, "You have already flagged this review.")
    review.update_hidden_status()
    return redirect("flowerproducts:product_detail", review.product.id)
