from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.forms import PasswordInput


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'specialization')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'class':'form-control mt-1', 'placeholder':'Email'}))
    first_name = forms.CharField(label="Имя", max_length=30, widget=forms.TextInput(attrs={'class':'form-control mt-1', 'placeholder':'Имя'}))
    last_name = forms.CharField(label="Фамилия", max_length=30, widget=forms.TextInput(attrs={'class':'form-control mt-1', 'placeholder':'Фамилия'}))
    specialization = forms.CharField(max_length=250, required=False, widget=forms.TextInput(attrs={'class':'form-control mt-1',  'placeholder':'Специализация'}))

    class Meta:
        model=User
        fields = ('first_name', 'last_name', 'email','specialization')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'class':'form-control mt-1',  'placeholder':'Пароль'})
        self.fields['password2'].widget = PasswordInput(attrs={'class':'form-control mt-1',  'placeholder':'Повторите пароль'})

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'class':'form-control mt-1', 'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mt-1',  'placeholder':'Пароль'}))
    class Meta:
        model=User
        fields = ('email')
