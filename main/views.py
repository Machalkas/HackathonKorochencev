from django.shortcuts import render, redirect
#from django.http import HttpResponse


def index(request):
    if request.user.is_authenticated:
        return redirect("/team/view")
    return render(request, "main/index.html")
    
