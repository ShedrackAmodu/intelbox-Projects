from django.db import models
from django.contrib.auth.models import User
import uuid, random
from django.utils import timezone

#check this to change password, if not needed remove it 
class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, blank=True, null=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.otp or self.token}"
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='front_product')

    class Meta:
        db_table = 'storefront_product'
    
    def __str__(self):
        return self.name



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    email_verification_code_created_at = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)  # Add this line

    def generate_email_verification_code(self):
        self.email_verification_code = str(random.randint(100000, 999999))
        self.email_verification_code_created_at = timezone.now()
        self.save()

    def verify_email_verification_code(self, code):
        if self.email_verification_code == code and self.email_verification_code_created_at >= timezone.now() - timezone.timedelta(minutes=5):
            self.email_verified = True
            self.email_verification_code =None
            self.save()
            return True
        return False
      
    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()

    def verify_otp(self, otp):
        if self.otp == otp:
            # Clear OTP after successful verification
            self.otp = None
            self.save()
            return True
        return False

    def __str__(self):
        return self.email
       # return self.user.username old uncase error arises

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # items field is defined with ManyToMany relationship through CartItem

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='Pending')
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'Order {self.payment_id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
