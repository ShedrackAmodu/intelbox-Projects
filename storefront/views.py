from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from .models import UserProfile, Order, Category, Cart, CartItem, Product
from .forms import UserProfileForm, UserForm, PasswordChangeForm, OrderForm, OrderItem, CustomUserCreationForm
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages 
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  
from .models import UserOTP
from random import randint
from django.core.mail import send_mail
#import logging


#logger = logging.getLogger(__name__)


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()[:10]  # Get first 10 products for simplicity, adjust as needed
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'storefront/home.html', context)

def category_view(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'storefront/home.html', {'categories': categories, 'products': products})

def search_view(request):
    categories = Category.objects.all()
    search_query = request.GET.get('search_query', '')
    products = Product.objects.filter(name__icontains=search_query)
    return render(request, 'storefront/home.html', {'categories': categories, 'products': products})


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


def product_list(request):
    products = Product.objects.all()
    return render(request, 'storefront/product_list.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile, created = UserProfile.objects.get_or_create(
                user=user, 
                email=user.email, 
                phone_number=form.cleaned_data['phone_number']
            )

            # Generate OTP
            otp = str(randint(100000, 999999))
            user_profile.otp = otp
            user_profile.save()

            # Send OTP via email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                'onlinestorea731@hotmail.com',
                [user.email],
                fail_silently=False,
            )

            return redirect('verify_otp')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'storefront/register.html', {'form': form})
 



def confirm_account(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        try:
            user_otp = UserOTP.objects.get(otp=otp)
            user = user_otp.user
            user.is_active = True
            user.save()
            user_otp.delete()  # Clean up OTP record
            messages.success(request, 'Your account has been confirmed.')
            return redirect('login')
        except UserOTP.DoesNotExist:
            messages.error(request, 'Invalid OTP.')
            return redirect('confirm_account')

    return render(request, 'confirm_account.html')


@csrf_exempt 
@login_required
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp:
            try:
                user_profile = UserProfile.objects.get(email=request.user.email)
                
                if user_profile.verify_otp(otp) or user_profile.verify_email_verification_code(otp):
                    print("good13")
                    # Handle successful OTP verification
                    return redirect('profile')  # Replace with appropriate redirect
                else:
                    print("bad")
                    messages.error(request, 'Invalid OTP. Please try again.')
            except UserProfile.DoesNotExist:
                print("user_profile")
                messages.error(request, 'User profile does not exist.')
        else:
            messages.error(request, 'OTP not provided.')
    
    return render(request, 'storefront/verify_otp.html')  # Replace with your template name
   
#@csrf_exempt  # If you use this, make sure to handle CSRF protection appropriately
@require_POST
@login_required
def update_cart(request):
    messages.success(request, 'Item added to cart successfully.')
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()   
        
        return JsonResponse({'message': 'Item added to cart successfully.'})
    
        
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

 
def get_cart_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = CartItem.objects.filter(cart_id = cart)
            cart_count = sum(item.quantity for item in cart_items)
        else:
            cart_count = 0

    return JsonResponse({'cart_count': cart_count})



def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
    return redirect('cart')

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
 
def order_success(request):
    return render(request, 'storefront/order_success.html' )


@login_required
def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        total_price = cart.total_price()
        print(f'Cart Items: {cart_items}')  # Debugging line
        print(f'Total Price: {total_price}')  # Debugging line
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0.0

    return render(request, 'storefront/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


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






#def cart_count_test(request):
#    if request.user.is_authenticated:
#        cart = Cart.objects.filter(user=request.user).first()
#        if cart:
#            cart_items = CartItem.objects.filter(cart_id = cart)
#            cart_count = sum(item.quantity for item in cart_items)
#        else:
#            cart_count = 0
#    else:
#        cart_count = 0
#    return JsonResponse({'cart_count': cart_count})