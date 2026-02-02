from django.urls import path, include

from . import views

app_name = "flowerproducts"

urlpatterns = [
    path("", views.index, name="index"),
    path("categories/", views.category_list, name="categories"),
    path("categories/<int:category_id>/", views.category_detail, name="category"),
    path("<int:product_id>/", views.product_detail, name="product_detail"),
    path("<int:product_id>/add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("search/", views.search_results, name="search_results"),
    path("", include("reviews.urls")),
]
