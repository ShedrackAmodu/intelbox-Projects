from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Order, OrderItem
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number']


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
       

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }



class PasswordChangeForm(DjangoPasswordChangeForm):
    class Meta:
        fields = ['old_password', 'new_password', 'confirm_password']
        widgets = {
            'old_password': forms.PasswordInput,
            'new_password': forms.PasswordInput,
            'confirm_password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("New password and confirm password do not match.")

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'total_price']
        
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=15, required=True, help_text='Required.')
    password1 = forms.CharField(max_length=32, required=True, help_text='Required.')
    password2 = forms.CharField(max_length=32, required=True, help_text='Required.')
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email','phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                email=self.cleaned_data['email']
            )
            if created:
                profile.generate_email_verification_code()  # Generate email verification code on profile creation

        return user
        


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Provide a valid email address.')     
 


class CheckoutForm(forms.Form):
    delivery_address = forms.CharField(label='Delivery Address', widget=forms.Textarea)
 