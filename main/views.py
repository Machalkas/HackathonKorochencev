from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from userAuth.models import User
from team.models import Teams
from .models import Settings, News
#from django.http import HttpResponse


def index(request):
    # if request.user.is_authenticated:
    #     user=User.objects.get(pk=request.user.pk)
    #     if user.is_specialist:
    #         return redirect("company")
    #     return redirect("/team")
    return render(request, "main/index.html")
    
def notFound(request, exception):
    # print(exception)
    return render(request, "main/404.html")
def serverError(request):
    # print(exception)
    return render(request, "main/500.html")

def listNews(request):
    n=News.objects.all()
    p=Paginator(n, 10)
    page=request.GET.get("page")
    try:
        post=p.page(page)
    except PageNotAnInteger:
        post=p.page(1)
    except EmptyPage:
        post=p.page(p.num_pages)
    for i in post:
        if len(i.text)>=100:
            i.text=i.text[:97]+"..."
    return render(request, "main/news.html", {"news":post,"max_pages":p.num_pages})

def viewNews(request, key):
    try:
        n=News.objects.get(id=key)
    except:
        return render(request, "main/news_view.html", {"news":None})
    return render(request, "main/news_view.html", {"news":n})

def manageMain(request):
    if request.is_ajax and request.method == "GET":
        action=request.GET.get('action')
        if action=="get-data":
            start_date,end_date=None,None
            users,teams=0,0
            try:
                s=Settings.objects.all()
                start_date=s[0].start_date
                end_date=s[0].end_date
            except:
                pass
            try:
                users=User.objects.filter(is_specialist=False).filter(is_superuser=False).count()
            except:
                pass
            try:
                teams=Teams.objects.all().count()
            except:
                pass
            return JsonResponse({'start-date':start_date, 'end-date':end_date, 'users-count':users, 'teams-count':teams}, status=200)