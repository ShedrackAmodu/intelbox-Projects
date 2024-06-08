from django.shortcuts import render
from .models import Product
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect


def product_list(request):
    products = Product.objects.all()
    return render(request, 'storefront/product_list.html', {'products': products})




def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        stock = request.POST.get('stock')
        if stock:
            product.stock = stock
            product.updated_at = timezone.now()
            product.save()
            return redirect('storefront/product_list')
    return render(request, 'storefront/update_product.html', {'product': product})