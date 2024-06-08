# Register your models here.
from django.contrib import admin
from  .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'stock', 'image_url')
    #readonly_fields = ('created_at', 'updated_at' )
 

#admin.site.register(Product, ProductAdmin)
