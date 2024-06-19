from django import forms
from .models import Product
from django.contrib.auth.models import User 

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price',  'image_url', 'stock', 'supplier','category' ]

     

class StaffPromotionForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")