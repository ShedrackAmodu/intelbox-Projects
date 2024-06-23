from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm 
from django.contrib.auth.decorators import login_required
from storefront.models import Product as StorefrontProduct 
from storefront.models import Order
from django.db.models import Q
import requests
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .forms import StaffPromotionForm

from django.contrib.admin.views.decorators import staff_member_required

from storefront.models import  Order  # Import your Order model

@staff_member_required
def admin_user_list(request):
    users = User.objects.all()
    return render(request, 'storeadmin/user_list.html', {'users': users})

@staff_member_required
def admin_order_list(request):
    pending_orders = Order.objects.exclude(status='delivered')
    return render(request, 'storeadmin/order_list.html', {'orders': pending_orders})

@staff_member_required
def admin_home(request):
    return render(request, 'storeadmin/home.html')



@staff_member_required
def delivered_orders(request):
    delivered_orders = Order.objects.filter(status='delivered')
    return render(request, 'storeadmin/delivered.html', {'delivered_orders': delivered_orders})

def product_list(request):
    query = request.GET.get('q')
    if query:
        products = StorefrontProduct.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        products = StorefrontProduct.objects.all()
   # products = StorefrontProduct.objects.all()  #used the storefront so it shows update time and created time 
    # also the admin is for the owner and trustees and user end has it for the employees interface as the outside world
    #have limited views but same app also 
    return render(request, 'storeadmin/product_list.html', {'products': products})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            # Create a corresponding StorefrontProduct instance
            StorefrontProduct.objects.create(
                id=product.id,  # Assuming id should be the same
                name=product.name,
                description=product.description,
                price=product.price,
                stock=product.stock,
                image_url=product.image_url
            )
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'storeadmin/add_product.html', {'form': form})

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        storefront_product = StorefrontProduct.objects.get(pk=pk)
    except StorefrontProduct.DoesNotExist:
        storefront_product = None

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            # Update the StorefrontProduct if it exists
            if storefront_product:
                storefront_product.name = product.name
                storefront_product.description = product.description
                storefront_product.price = product.price
                storefront_product.stock = product.stock
                storefront_product.image_url = product.image_url
                storefront_product.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'storeadmin/edit_product.html', {'form': form})


def delete_product(request, pk):
    # Fetch the product from the admin data/products
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        # Attempt to delete the product from admin data/products
        try:
            product.delete()
            # Attempt to delete the corresponding product from the front data/products
            try:
                front_product = StorefrontProduct.objects.get(pk=pk)
                front_product.delete()
            except StorefrontProduct.DoesNotExist:
                pass  # If the product does not exist in the front data, it's not an issue

           # messages.success(request, 'Product deleted successfully.')
            return redirect('product_list')
        except Exception as e:
            pass
          #  messages.error(request, f'Error deleting product: {e}')
    
    return render(request, 'storeadmin/delete_product.html', {'product': product})
 


# Only allow access to superusers
@user_passes_test(lambda u: u.is_superuser)
def promote_to_staff(request):
    if request.method == 'POST':
        form = StaffPromotionForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            user.is_staff = True
            user.save()
            return redirect('promote_to_staff')
    else:
        form = StaffPromotionForm()
    
    return render(request, 'storeadmin/promote_to_staff.html', {'form': form})


def fetch_data_from_api(request):
    """
    This view fetches data from an external API and renders it in a template.
    """
    # API endpoint to fetch data from
    api_url = 'https://fakestoreapi.com/products'
    
    # Make a GET request to the API
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
    else:
        # If the request failed, set data to None
        data = None

    # Render the data in the template 'myapp/api_data.html'
    return render(request, 'storeadmin/api_data.html', {'data': data})
 