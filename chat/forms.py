from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email','name', 'password1', 'password2')

class SignInForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField( widget= forms.PasswordInput())