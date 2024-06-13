from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from .models import UserProfile, Order, Category, Cart, CartItem, Product
from .forms import UserProfileForm, UserForm, PasswordChangeForm, OrderForm, OrderItem, CustomUserCreationForm
from django.http import JsonResponse
from django.core.mail import send_mail
from decimal import Decimal 
from django.template.loader import render_to_string
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'storefront/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()[:10]  # Get first 10 products for simplicity, adjust as needed
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'storefront/home.html', context)

def get_products_by_category(request, category_id):
    products = Product.objects.filter(category_id=category_id)
    product_data = [{'name': product.name, 
                     'description': product.description, 
                     'price': product.price,
                     'image_url': product.image_url} 
                    for product in products]
    
    return JsonResponse({'products': product_data})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'storefront/product_list.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user, email=user.email, phone_number=form.cleaned_data['phone_number'])
            login(request, user)
            return redirect('profile')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'storefront/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'storefront/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
 
 
 
@login_required
def change_password(request):
    print("Request User:", request.user)  # Debugging output
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        print("Password Form Data:", request.POST)  # Debugging output
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        password_form = PasswordChangeForm(request.user)
    return render(request, 'storefront/change_password.html', {
        'password_form': password_form
    })

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'storefront/create_order.html', {'form': form})

@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'storefront/order_detail.html', {'order': order})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, defaults={'user': request.user})
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user, defaults={'user': request.user})
    return render(request, 'store/cart.html', {'cart': cart})


def order_success(request):
    return redirect('storefront/order_success')

def process_payment(total_price):
    # Pseudo-code for payment processing
    # Replace this with actual payment gateway integration
    payment_id = 'dummy_payment_id'
    payment_status = 'Success'
    return payment_id, payment_status


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart.items.all())

    if request.method == 'POST':
        # Check stock availability
        for item in cart.items.all():
            if item.product.stock < item.quantity:
                return render(request, 'store/checkout.html', {
                    'cart': cart,
                    'total_price': total_price,
                    'error': f"Sorry, we don't have enough stock for {item.product.name}."
                })

        # Process payment (pseudo-code, replace with actual payment integration)
        payment_id, payment_status = process_payment(total_price)

         
    if payment_status == 'Success':
    # Create order
        order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        payment_id=payment_id,
        payment_status=payment_status
    )

    # Update product stock
    for item in cart.items.all():
        product = item.product
        product.stock -= item.quantity
        product.save()
        # Add to order (optional: create OrderItem model)

    # Send email notification to user
    send_mail(
        'Order Confirmation',
        f'Thank you for your order. Your order ID is {order.id}.',
        'your-email@example.com',
        [request.user.email],
        fail_silently=False,
    )

    # Send email notification with order details
    order_items = OrderItem.objects.filter(order=order)
    order_details = {
        'order_id': order.id,
        'user_email': request.user.email,
        'total_price': total_price,
        'order_items': order_items,
    }
    email_subject = 'Order Details'
    email_body = render_to_string('email/order_details_email.html', order_details)
    send_mail(
        email_subject,
        email_body,
        'your-email@example.com',
        [request.user.email],
        fail_silently=False,
    )

    # Clear cart
    cart.items.all().delete()

    return redirect('order_success')
        