from django.urls import path
from . import views
 

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
    path('cart/update/', views.update_cart, name='update_cart'),
     path('category/<int:category_id>/', views.category_view, name='category'),
    path('search/', views.search_view, name='search'),
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),
    #path('cart-count',views.cart_count_test, name= 'cart_count_test') 
      
]
