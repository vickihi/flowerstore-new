from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name
