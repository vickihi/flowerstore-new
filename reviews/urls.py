from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("<int:product_id>/add/", views.add_review, name="add_review"),
    path("<int:review_id>/vote/", views.add_vote, name="add_vote"),
    path("<int:review_id>/comment/", views.add_comment, name="add_comment"),
    path("<int:review_id>/flag/", views.add_flag, name="add_flag"),
]
