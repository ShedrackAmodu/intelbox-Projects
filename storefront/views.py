from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from .models import UserProfile, Order, Category, Cart, CartItem, Product
from storeadmin.models import Product as adminProduct
from .forms import UserProfileForm, UserForm, PasswordChangeForm, OrderForm, OrderItem, CustomUserCreationForm, CustomPasswordResetForm 
from .forms import CheckoutForm, PasswordResetForm, OrderForm
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages 
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  
from .models import UserOTP
from random import randint 
from django.contrib import messages   
from django.contrib.auth.models import User 
from .models import UserProfile, UserOTP 
from uuid import uuid4
import time
from django.core.mail import EmailMessage 
from django.conf import settings
import os 
  
 
 

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
            # Generate and save OTP and email verification code
            user_profile.generate_otp()
            user_profile.generate_email_verification_code()

            # Send OTP and email verification code via email
            send_mail(
                'Your OTP Code and Email Verification Code',
                f'Your OTP code is {user_profile.otp}\nYour email verification code is {user_profile.email_verification_code}',
                'onlinestorea731@hotmail.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Registration successful. Please check your email for OTP and email verification code.')
            return redirect('confirm_account')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'storefront/register.html', {'form': form})
    
@login_required
def change_password(request):
    if not request.user.userprofile.email_verified:
        messages.error(request, 'You must verify your email before changing your password.')
        return redirect('verify_otp')

    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        password_form = PasswordChangeForm(request.user)
    return render(request, 'storefront/change_password.html', {'password_form': password_form})


def forgot_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                user_otp, created = UserOTP.objects.get_or_create(user=user)
                user_otp.otp = str(randint(100000, 999999))
                user_otp.token = uuid4()
                user_otp.save()

                # Send OTP and token via email
                send_mail(
                    'Reset Your Password',
                    f'Your OTP code is {user_otp.otp}\nYour password reset token is {user_otp.token}',
                    'onlinestorea731@hotmail.com',  # Replace with your sender email
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'An email with OTP and token has been sent to reset your password.')
                return redirect('reset_password')
            except User.DoesNotExist:
                messages.error(request, 'No user found with this email address.')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'storefront/forgot_password.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            token = request.POST.get('token')
            otp = request.POST.get('otp')
            new_password = request.POST.get('new_password')
            try:
                user_otp = UserOTP.objects.get(token=token, otp=otp)
                user = user_otp.user
                user.set_password(new_password)
                user.save()
                user_otp.delete()  # Clean up OTP record
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login')
            except UserOTP.DoesNotExist:
                messages.error(request, 'Invalid token or OTP.')
    else:
        form = PasswordResetForm()
    return render(request, 'storefront/reset_password.html', {'form': form})




#@csrf_exempt  # If you use this, make sure to handle CSRF protection appropriately
@require_POST
@login_required
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()   
        if 'HTTP_REFERER' in request.META:
            referer = request.META['HTTP_REFERER']
            if 'cart' in referer:  # Check if 'cart' is in the referer URL
                time.sleep(2)
                return redirect('cart')  # Redirect to the cart page if request came from there
        
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
        time.sleep(2)
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

    # Fetch orders for the logged-in user
    orders = Order.objects.filter(user=request.user)

    return render(request, 'storefront/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'orders': orders,
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
                # Send email notification to user (plain text)
            send_mail(
                    'Order Confirmation',
                    f'Thank you for your order. Your order ID is {order.id}.',
                    'onlinestorea731@hotmail.com',
                    [request.user.email],
                    fail_silently=False,
                )
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'storefront/create_order.html', {'form': form})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    is_staff = request.user.is_staff
    form = None
    
    if request.method == 'POST' and is_staff:
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order status updated successfully.')
            return redirect('order_detail', order_id=order_id)
    elif order.status != 'delivered':  # Only create form if status is not delivered
        form = OrderForm(instance=order)
    return render(request, 'storefront/order_detail.html', {
        'order': order,
        'order_items': order_items,
        'form': form,  # Pass form to template for staff users
        'is_staff': is_staff  # Pass is_staff flag to template
    })
 
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
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        total_price = cart.total_price()
        error_message = None
        form = CheckoutForm()

        if request.method == 'POST':
            form = CheckoutForm(request.POST)
            if form.is_valid(): 
                delivery_address = form.cleaned_data.get('delivery_address')
                city = form.cleaned_data.get('city')

                # Check stock availability
                insufficient_stock_items = []
                for item in cart_items:
                    if item.product.stock < item.quantity:
                        insufficient_stock_items.append(item.product)

                if insufficient_stock_items:
                    error_message = f"Sorry, we don't have enough stock for the following items:\n"
                    for item in insufficient_stock_items:
                        error_message += f"{item.name}: Available {item.stock} items\n"

                if error_message:
                    return render(request, 'storefront/checkout.html', {
                        'cart': cart,
                        'cart_items': cart_items,
                        'total_price': total_price,
                        'error': error_message,
                        'form': form,
                    })

                # Process payment (pseudo-code, replace with actual payment integration)
                payment_id, payment_status = process_payment(total_price)

                if payment_status == 'Success':
                    # Create order
                    order = Order.objects.create(
                        user=request.user,
                        total_price=total_price,
                        payment_id=payment_id,
                        payment_status=payment_status,
                        delivery_address = delivery_address,
                        city=city
                    )

                    # Update product stock and create OrderItem
                    for item in cart_items:
                        product = item.product
                        product.stock -= item.quantity
                        AdminProduct = adminProduct.objects.get(name=product)  # Assumes adminProduct is linked to product
                        AdminProduct.stock -= item.quantity
                        product.save()
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=item.quantity,
                            price=product.price
                        )

                    # Send email notification with order details (plain text)
                    order_details = {
                        'order_id': order.id,
                        'user_email': order.user.email,
                        'total_price': order.total_price,
                        'order_items': OrderItem.objects.filter(order=order),
                    }
                    email_subject = 'Order Confirmation'
                    email_body = render_to_string('storefront/order_details_email.html', order_details)
                    
                    html_file_path = os.path.join(settings.BASE_DIR, 'order_confirmation.html')
                    with open(html_file_path, 'w', encoding='utf-8') as html_file:
                        html_file.write(email_body)

                    # Attach the HTML file to the email
                    email = EmailMessage(
                        email_subject,
                        'Please see the attached order confirmation.',
                        'onlinestorea731@hotmail.com',  # Replace with your sender email
                        [order.user.email],         # Send to the user's email
                    )
                    email.attach_file(html_file_path)

                    # Send the email
                    email.send(fail_silently=False)

                    # Optionally, delete the temporary HTML file after sending the email
                    os.remove(html_file_path)

                    # Clear cart
                    cart_items.delete()

                    return redirect('order_success')

        return render(request, 'storefront/checkout.html', {
                'cart': cart,
                'cart_items': cart_items,
                'total_price': total_price,
                'form': form,
                'error': error_message,})

    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0.0

    return render(request, 'storefront/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })
 
    
    
@login_required
def my_orders(request):
    pending_orders = Order.objects.filter(user=request.user, status='pending')
    delivered_orders = Order.objects.filter(user=request.user, status='delivered')
    return render(request, 'storefront/my_orders.html', {
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
    })

@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'confirmed','delivered']:
            order.status = new_status
            order.save()
    return redirect('order_detail', order_id=order.id)
 

@csrf_exempt 
def confirm_account(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email_verification_code = request.POST.get('email_verification_code')  # Assuming you're collecting this from the form
        
        if otp and email_verification_code:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                
                if user_profile.verify_otp(otp) and user_profile.verify_email_verification_code(email_verification_code):
                    user_profile.email_verified = True
                    user_profile.save()
                    messages.success(request, 'Your account has been confirmed.')
                    return redirect('profile')  # Redirect to profile or another appropriate page
                else:
                    messages.error(request, 'Invalid OTP or email verification code. Please try again.')
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile does not exist.')
        else:
            messages.error(request, 'OTP and email verification code are required.')

    return render(request, 'storefront/confirm_account.html')  # Replace with your template name



@login_required
def resend_codes(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.generate_otp()
        user_profile.generate_email_verification_code()

        # Send OTP and email verification code via email
        send_mail(
            'Your OTP Code and Email Verification Code',
            f'Your OTP code is {user_profile.otp}\nYour email verification code is {user_profile.email_verification_code}',
            'onlinestorea731@hotmail.com',
            [user_profile.email],
            fail_silently=False,
        )

        messages.success(request, 'OTP and email verification code have been resent to your email.')
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile does not exist.')

    return redirect('confirm_account')
