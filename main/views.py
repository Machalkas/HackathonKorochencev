from django.shortcuts import render, redirect
from userAuth.models import User
#from django.http import HttpResponse


def index(request):
    if request.user.is_authenticated:
        user=User.objects.get(pk=request.user.pk)
        if user.is_specialist:
            return redirect("company/view")
        return redirect("/team/view")
    return render(request, "main/index.html")
    
