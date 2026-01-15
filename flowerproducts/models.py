from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name



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

