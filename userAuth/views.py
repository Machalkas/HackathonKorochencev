from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, SignUpForm

from django.http import HttpResponse

def join(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if  form.is_valid():
            user=form.save()
            user.save()
            email = form.cleaned_data.get('email')
            user_pass = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=user_pass)
            logout(request)
            login(request, user)
            return redirect('/')
        else:
            print(form.errors)

    else:
        form = SignUpForm()
    return render(request, 'userAuth/join.html', {'form':form})