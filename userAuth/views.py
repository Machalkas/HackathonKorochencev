from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from django.http import JsonResponse, HttpResponse
from .models import User
from django.core.mail import send_mail


# def join(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if  form.is_valid():
#             user=form.save()
#             user.save()
#             email = form.cleaned_data.get('email')
#             user_pass = form.cleaned_data.get('password1')
#             user = authenticate(email=email, password=user_pass)
#             logout(request)
#             login(request, user)
#             url=request.GET.get('next','/')
#             return redirect(url) 
#     else:
#         form = SignUpForm()
#     return render(request, 'userAuth/join.html', {'form':form})
def sendForm(request):
    if request.method=="GET":
        login_form=LoginForm()
        singup_form=SignUpForm()
        return render(request, 'userAuth/auth.html', {"login_form":login_form, "singup_form":singup_form})

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
    return redirect('/auth')    

def profile(request, key=None):
    if key==None:
        user=request.user
    else:
        try:
            user=User.objects.get(pk=key)
        except:
            user=request.user
    return render(request, "userAuth/profile.html", {"user":user})

def ajax(request):
    if request.is_ajax and request.method=="POST":
        action=request.POST.get('action')
        if action=='login':
            form=LoginForm(request.POST)
            if form.is_valid():
                email=form.cleaned_data.get('email')
                user_pass=form.cleaned_data.get('password')
                user = authenticate(email=email, password=user_pass)
                if user!=None and user.is_active:
                    login(request, user)
                    url=request.GET.get('next','/')
                    return JsonResponse({"url":url}, status=200)
                else:
                    return JsonResponse({"error":"Не правильный логин или пароль"}, status=400)
            else:
                return JsonResponse({"error":form.errors}, status=400)
        elif action=='singup':
            form=SignUpForm(request.POST)
            if form.is_valid():
                user=form.save()
                user.save()
                email = form.cleaned_data.get('email')
                user_pass = form.cleaned_data.get('password1')
                user = authenticate(email=email, password=user_pass)
                logout(request)
                login(request, user)
                url=request.GET.get('next','/')
                send_mail('Хакатон Регистрация', 'Вы были зарегистрированны на Хакатон', '', ['al1999dk@gmail.com'], fail_silently=False)
                return JsonResponse({"url":url}, status=200)
            else:
                return JsonResponse({"error":form.errors}, status=400)
    else:
        return HttpResponse("Уйди, разбойник")
                    