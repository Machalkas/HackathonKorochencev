from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# from .forms import UserForm, ProfileForm
from django.http import HttpResponse

def join(request):
    return HttpResponse('<h1>hello')
    # if request.method == 'POST':
    #     user_form = UserForm(request.POST)
    #     profile_form = ProfileForm(request.POST)
    #     if user_form.is_valid() and profile_form.is_valid():
    #         user=user_form.save()
    #         user.save()
    #         profile=profile_form.save()
    #         profile.save()
    #         username = user_form.cleaned_data.get('username')
    #         user_pass = user_form.cleaned_data.get('password1')
    #         user = authenticate(username=username, password=user_pass)
    #         login(request, user)
    #         return redirect('/')
    # else:
    #     user_form = UserForm()
    #     profile_form = ProfileForm()
    # return render(request, 'userAuth/signUp.html', {'user_form': user_form, 'profile_form':profile_form})