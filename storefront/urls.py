from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('update/<int:product_id>/', views.update_product, name='update_product'),
]



 