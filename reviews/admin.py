from django.contrib import admin
from reviews.models.review import Review
from reviews.models.vote import Vote
from reviews.models.comment import Comment
from reviews.models.flag import Flag

# Register your models here.
admin.site.register(Review)
admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(Flag)
