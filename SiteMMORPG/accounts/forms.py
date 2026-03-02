# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django import forms


# class BaseRegisterForm(UserCreationForm):
#     email = forms.EmailField(label = "Email")
#     first_name = forms.CharField(label = "Имя")
#     last_name = forms.CharField(label = "Фамилия")
#     class Meta:
#         model = User
#         fields = ("username", 
#                   "first_name", 
#                   "last_name", 
#                   "email", 
#                   "password1", 
#                   "password2", )


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
