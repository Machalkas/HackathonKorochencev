from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
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
            url=request.GET.get('next','/')
            return redirect(url) 
    else:
        form = SignUpForm()
    return render(request, 'userAuth/join.html', {'form':form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            user_pass=form.cleaned_data.get('password')
            user = authenticate(email=email, password=user_pass)
            if user!=None and user.is_active:
                    login(request, user)
                    url=request.GET.get('next','/')
                    return redirect(url)   
            else:
                pass        
    else:
        form = LoginForm()
    return render(request, 'userAuth/login.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('/')    