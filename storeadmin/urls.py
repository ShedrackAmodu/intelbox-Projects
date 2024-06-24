from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('products/', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('api_data/', views.fetch_data_from_api, name='api_data'),
   # path('promote_to_staff/', views.promote_to_staff, name='promote_to_staff'),
    path('users/', views.admin_user_list, name='admin_user_list'),  # Add this line
    path('orders/', views.admin_order_list, name='admin_order_list'),  # Add this line
    path('delivered/', views.delivered_orders, name='delivered_orders'),
    path('manage_users/', views.manage_users, name='manage_users'),
    # path('promote_to_staff/<int:user_id>/', views.promote_to_staff, name='promote_to_staff'),
]
