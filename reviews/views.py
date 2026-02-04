from django.shortcuts import get_object_or_404, redirect, render
from django.db import IntegrityError
from django.contrib import messages
from django.core.exceptions import ValidationError

from flowerproducts.models import Product
from reviews.models.review import Review
from .forms import ReviewForm, VoteForm


def add_review(request, product_id):
    if request.method != "POST":
        return redirect("flowerproducts:product_detail", product_id)

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

    return redirect("flowerproducts:product_detail", product_id)


# Vote ========================================
def create_vote(request, review_id):
    """Show form to create a vote."""
    review = get_object_or_404(Review, pk=review_id)
    review_list = Review.objects.filter(product=review.product)
    
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

    


