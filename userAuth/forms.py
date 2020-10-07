from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(label="Имя", max_length=30)
    last_name = forms.CharField(label="Фамилия", max_length=30)
    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'specialization')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)

# class SignUpForm(forms.ModelForm):
#     email = forms.EmailField(max_length=254)
#     first_name = forms.CharField(label="Имя", max_length=30)
#     last_name = forms.CharField(label="Фамилия", max_length=30)

#     class Meta:
#         model=User
#         fields = ('first_name', 'last_name', 'email','specialization','password1','password2')