from django import forms
from .models import Product
from django.contrib.auth.models import User 

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price',  'image_url', 'stock', 'supplier','category' ]

     

class StaffPromotionForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Select User")
    

class PromoteToStaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_staff'].label = 'Promote/Demote to Staff'
        self.fields['is_staff'].help_text = 'Check to promote to staff, uncheck to demote.'