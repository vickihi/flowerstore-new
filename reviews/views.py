from django.shortcuts import get_object_or_404, redirect
from django.db import IntegrityError
from django.contrib import messages

from flowerproducts.models import Product
from .forms import ReviewForm


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
