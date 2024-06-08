from django.db import models
from storefront.models import Category
from django.dispatch import receiver
from django.db.models.signals import post_save
from storefront.models import Product as StorefrontProduct 
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='admin_products')  # Specify a distinct related_name
    #image_url = models.URLField()
    image_url = models.CharField(max_length=255)  # or FilePathField
    stock = models.IntegerField(default=0)
    supplier = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        

@receiver(post_save, sender=Product)
def update_storefront(sender, instance, created, **kwargs):
     # Only update storefront if the instance was updated, not created
        try:
            storefront_product = StorefrontProduct.objects.get(id=instance.id)
        except StorefrontProduct.DoesNotExist:
            storefront_product = StorefrontProduct()
            storefront_product.id = instance.id
            storefront_product.created_at = timezone.now()
        storefront_product.name = instance.name
        storefront_product.description = instance.description
        storefront_product.stock = instance.stock
        storefront_product.price = instance.price
        storefront_product.image_url = instance.image_url
        storefront_product.updated_at = timezone.now()
        # Update more fields as needed
        storefront_product.save()