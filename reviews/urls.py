from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path(
        "<int:product_id>/add/",
        views.add_review,
        name="add_review",
    ),
]
