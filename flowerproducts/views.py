from django.shortcuts import render
from .models import Product
from .forms import IndexForm
 
# Create your views here.
def index(request):
    form = IndexForm(request.GET)

    sort_order = IndexForm.SORT_ORDERS[0][0]
    filter_category = None
    products = Product.objects.available()

    if form.is_valid():
        sort_order = form.cleaned_data.get("sort_order") or sort_order
        filter_category = form.cleaned_data.get("filter_category")

    if filter_category:
        products = products.filter(category_id=filter_category)

    products = products.order_by(sort_order)

    return render(
        request,
        "flowerproducts/index.html",
        {
            "products": products,
            "form": form,
        }
    )

