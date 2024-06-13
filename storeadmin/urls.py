from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('api_data/', views.fetch_data_from_api, name='api_data'),
   # path('admin/update/<int:product_id>/', views.admin_update_product, name='admin_update_product'),

]
