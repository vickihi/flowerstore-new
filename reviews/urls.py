from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path(
        "<int:product_id>/add/",
        views.add_review,
        name="add_review",
    ),
    path(
        "<int:review_id>/vote/",
        views.create_vote,
        name="create_vote",
    ),
    path(
        "<int:review_id>/vote/submit/",
        views.create_vote_submit,
        name="create_vote_submit",
    ),
    path(
        "<int:review_id>/comment/",
        views.add_comment,
        name="add_comment",
    ),
    path("<int:review_id>/flag/",
         views.create_flag,
         name="create_flag"
    ),
    path(
        "<int:review_id>/flag/submit/",
        views.create_flag_submit,
        name="create_flag_submit",
    ),
]
