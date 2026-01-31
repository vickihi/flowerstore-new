from typing import Self
from django.db import models


class ProductQuerySet(models.QuerySet):
    def available(self) -> Self:
        return self.filter(quantity__gt=0)

    def search(self, query: str) -> Self:
        return self.filter(name__icontains=query)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    objects = ProductQuerySet.as_manager()

    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="flowerproducts/")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField("created at", auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    views_count = models.PositiveIntegerField(default=0)  # add this field for sorting

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self):
        return self.name

    @property
    def is_available(self):
        """Convenience property for templates and admin.
        Avoid using this for queryset filtering.
        """
        return self.quantity > 0
    
    @classmethod
    def query_with_form(cls, products, cleaned_data):
        sort_order = cleaned_data["sort_order"] or "-created_at"  
        available = cleaned_data["available"]
        filter_category = cleaned_data["filter_category"]

        if available:
            products = products.available()

        if filter_category:
            products = products.filter(category=filter_category)
        
        if sort_order:
            products = products.order_by(sort_order)

        return products

 