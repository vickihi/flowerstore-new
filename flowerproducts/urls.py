from django.urls import path
from . import views

app_name = "flowerproducts"

urlpatterns = [
    path("", views.index, name="index"),
    # path("category/<int:category_id>/", views.category_detail, name="category_detail"),
    # path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    # path("search/", views.search, name="search"),
]
