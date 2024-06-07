from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    #TODO image_url check it
    
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('home_appliances', 'Home Appliances'),
        ('books', 'Books'),
        ('beauty_and_health', 'Beauty and Health'),
        ('sports_and_outdoors', 'Sports and Outdoors'),
        ('toys_and_games', 'Toys and Games'),
        ('furniture', 'Furniture'),
        ('automotive', 'Automotive'),
        ('groceries', 'Groceries'),
        # Add more categories as needed
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField()

    updated_at =   models.DateTimeField()

    categories = models.ManyToManyField(Category, related_name='front_products')  # Specify a distinct related_name
    #category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image_url = models.URLField()

    class Meta:
        db_table = 'storefront_product'
    
    def __str__(self):
        return self.name
    

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name} - {self.category.name}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields as needed, e.g., profile picture, address, etc.

    def __str__(self):
        return self.user.username