from django.contrib import admin
from .models import Category, Product, Order, OrderItem , Cart, CartItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'stock', 'created_at', 'updated_at', 'image_url')
    readonly_fields = ('created_at', 'updated_at' )
 

#admin.site.register(Product, ProductAdmin)


#admin.site.register(Category) 
#admin.site.register(Order)
#admin.site.register(OrderItem) 


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'stock', 'image_url')

 

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')