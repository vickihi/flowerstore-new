from django.db import models

# Create your models here.
class Category(models.Model):
    ...

class Product(models.Model):
    name = models.CharField()
    description = models.TextField()
    image = models.ImageField(upload_to='flowerproducts/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at', 'name']

    def __str__(self):
        return self.name