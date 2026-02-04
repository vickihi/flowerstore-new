from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from flowerproducts.models import Product
from reviews.models.review import Review
from .forms import ReviewForm, VoteForm, CommentForm


def add_review(request, product_id):
    """Handle form to add review to a product."""
    if request.method != "POST":
        return redirect("flowerproducts:product_detail", product_id=product_id)

    product = get_object_or_404(Product, pk=product_id)
    form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        try:
            review.save()
        except IntegrityError:
            messages.error(
                request, "You have already reviewed this product with this email."
            )
    else:
        messages.error(request, "Review form is invalid. Please check your input.")

    return redirect("flowerproducts:product_detail", product_id=product_id)


# Vote ========================================
def create_vote(request, review_id):
    """Show form to create a vote."""
    review = get_object_or_404(Review, pk=review_id)
    # review_list = Review.objects.filter(product=review.product)

    form = VoteForm()
    context = {"form": form, "review": review}
    return render(request, "reviews/create_vote.html", context)


def create_vote_submit(request, review_id):
    """Handle form to create a vote."""
    review = get_object_or_404(Review, pk=review_id)
    form = VoteForm(request.POST)

    if not form.is_valid():
        context = {"form": form, "review": review}
        return render(request, "reviews/create_vote.html", context)

    vote = form.save(commit=False)
    vote.review = review

    try:
        vote.full_clean()
    except ValidationError as e:
        form.add_error(None, e)
        context = {"form": form, "review": review}
        return render(request, "reviews/create_vote.html", context)

    vote.save()
    return redirect("flowerproducts:product_detail", review.product.id)


# Comment
def add_comment(request, review_id):
    """Add comment to review."""
    if request.method != "POST":
        return redirect("flowerproducts:index")

    review = get_object_or_404(Review, pk=review_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.review = review
        comment.save()
    else:
        messages.error(request, "There was an error with your comment.")
    return redirect("flowerproducts:product_detail", review.product.id)
