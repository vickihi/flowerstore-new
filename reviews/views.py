from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from flowerproducts.models import Product
from reviews.models.review import Review
from .forms import ReviewForm, VoteForm, CommentForm, FlagForm


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
    form = VoteForm()
    context = {"form": form, "review": review}
    return render(request, "reviews/create_vote.html", context)


def create_vote_submit(request, review_id):
    """Handle form to create a vote."""
    review = get_object_or_404(Review, pk=review_id)

    vote = Vote(review=review)
    form = VoteForm(request.POST, instance=vote)

    if not form.is_valid():
        context = {"form": form, "review": review}
        return render(request, "reviews/create_vote.html", context)

    form.save()
    return redirect("flowerproducts:product_detail", review.product.id)


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


def flag_review(request, review_id):
    """Flag review."""
    review = get_object_or_404(Review, pk=review_id)
    if request.method == "POST":
        form = FlagForm(request.POST)

        if form.is_valid():
            flag = form.save(commit=False)
            flag.review = review

            try:
                flag.full_clean()
                flag.save()
                messages.success(request, "Review flagged successfully.")
                return redirect("flowerproducts:product_detail", review.product.id)

            except ValidationError as e:
                if 'email' in e.message_dict:
                    form.add_error('email', e.message_dict['email'])
                else:
                    form.add_error(None, e)

            except IntegrityError:
                form.add_error('email', "You have already flagged this review.")

    else:
        form = FlagForm()

    return render(
        request,
        "reviews/flag.html",
        {"form": form, "review": review},
    )
