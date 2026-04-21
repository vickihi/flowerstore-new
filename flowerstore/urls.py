from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import products.views

urlpatterns = [
    path("", products.views.index, name="home"),
    path("products/", include("products.urls")),
    path("reviews/", include("reviews.urls")),
    path("orders/", include("orders.urls")),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
