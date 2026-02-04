from django.contrib import admin
from .models.review import Review
from reviews.models.vote import Vote

# Register your models here.
admin.site.register(Review)
admin.site.register(Vote)
