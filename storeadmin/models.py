from django.db import models
from storefront.models import Category

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='admin_products')  # Specify a distinct related_name
    image_url = models.URLField()
    inventory_count = models.IntegerField(default=0)
    supplier = models.CharField(max_length=100)

    def __str__(self):
        return self.name
