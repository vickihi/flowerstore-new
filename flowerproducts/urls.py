from django.urls import path
from . import views

app_name = "flowerproducts"

urlpatterns = [
    path("", views.index, name="home"),                            
]
