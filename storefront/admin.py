from django.contrib import admin
from .models import Category, Product, ProductCategory, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'stock', 'created_at', 'updated_at', 'image_url')
    readonly_fields = ('created_at', 'updated_at' )
 

admin.site.register(Product, ProductAdmin)


admin.site.register(Category) 
admin.site.register(ProductCategory)
admin.site.register(Order)
admin.site.register(OrderItem) 