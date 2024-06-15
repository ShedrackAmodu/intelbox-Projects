# context_processors.py
from .models import CartItem, Cart
#so it displays upon firs page load as at then the addtocart is not enabled but added another to the script in home
# so this is no longer needed, the enablement of this  commented out too in settings.py
def cart_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = CartItem.objects.filter(cart_id = cart)
            cart_count = sum(item.quantity for item in cart_items)
        else:
            cart_count = 0
    else:
        cart_count = 0
    return {'cart_count': cart_count}
