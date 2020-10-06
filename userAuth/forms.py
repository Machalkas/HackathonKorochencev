# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import Profile

# class UserForm(UserCreationForm):
#     email=forms.EmailField(max_length=254)
#     first_name = forms.CharField(label="Имя", max_length=30)
#     last_name = forms.CharField(label="Фамилия", max_length=30, required=False)
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

# class ProfileForm(UserCreationForm):
#     #specialization = forms.CharField(label="Направление", max_length=250)
#     class Meta:
#         model = Profile
#         fields = ('specialization',)


