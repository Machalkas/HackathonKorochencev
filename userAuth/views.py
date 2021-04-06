from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from django.http import JsonResponse, HttpResponse, Http404
from .models import User
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from team.urlGenerator import generate


def generateToken():
    count=0
    size=20
    while True:
        count+=1
        if count>50:
            size+=1
        # print(size)
        s=generate(size=size)
        try:
            t=User.objects.get(reset_token=s)
        except:
            return s

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

def resetPassPage(request, token=None):
    if token==None:
        return render(request, "userAuth/reset_password_email.html")
    try:
        User.objects.get(reset_token=token)
    except:
        raise Http404()
    return render(request, "userAuth/set_new_pass.html")

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
                    logout(request)
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
                # send_mail('Хакатон | Регистрация', 'Вы были зарегистрированны на Хакатон', '', [email], fail_silently=True)
                
                return JsonResponse({"url":url}, status=200)
            else:
                return JsonResponse({"error":form.errors}, status=400)
        elif action=="reset-password-email":
            e=request.POST.get("email")
            try:
                u=User.objects.get(email=e)
            except:
                return JsonResponse({"error":"Пользователь с таким email не найден"}, status=404)
            u.reset_token=generateToken()
            u.save()
            try:
                # send_mail('Хакатон | Востановление пароля', '<table>Для востановления пароля перейдите по <a href="">ссылке</a></table>', '', [e], fail_silently=False)
                subject, from_email, to = 'Востановление пароля', '', e
                text_content = 'Для востановления пароля перейдите по ссылке: '+request.META['HTTP_ORIGIN']+reverse("set_new_pass", args=[u.reset_token])
                html_content = '<table>Для востановления пароля перейдите по <a href="'+request.META['HTTP_ORIGIN']+reverse("set_new_pass", args=[u.reset_token])+'">ссылке</a></table>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except:
                return JsonResponse({"error":"Не удается отправить email"}, status=501)
            return JsonResponse({"ok":""})
        elif action=="set-new-password":
            try:
                u=User.objects.get(reset_token=request.POST.get("token"))
            except:
                return JsonResponse({"error":"Не верный токен"}, status=404)
            if not u.check_password(request.POST.get("password")):
                u.set_password(request.POST.get("password"))
                u.reset_token=""
                u.save()
                return JsonResponse({"ok":""})
            return JsonResponse({"error":"Пароль не валиден"}, status=400)
    else:
        return HttpResponse("Уйди, разбойник")
