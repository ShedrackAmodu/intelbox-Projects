from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Order, OrderItem

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email']  # Include any other fields you want to update



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("New password and confirm password do not match.")
        

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'total_price']  # Include fields relevant to your order

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']  # Include fields relevant to your order item

