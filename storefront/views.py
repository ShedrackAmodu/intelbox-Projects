from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .models import UserProfile, Order, OrderItem, Product, Category
from .forms import UserProfileForm, UserForm, PasswordChangeForm, OrderForm, OrderItemForm


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()[:10]  # Get first 10 products for simplicity, adjust as needed
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'storefront/home.html', context)
    

def product_list(request):
    products = Product.objects.all()
    return render(request, 'storefront/product_list.html', {'products': products})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, email=user.email)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'storefront/register.html', {'form': form})

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('storefront/profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                return redirect('profile')
            else:
                form.add_error('old_password', 'Old password is incorrect.')
    else:
        form = PasswordChangeForm()
    return render(request, 'change_password.html', {'form': form})

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
    return render(request, 'create_order.html', {'form': form})

@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_detail.html', {'order': order})
