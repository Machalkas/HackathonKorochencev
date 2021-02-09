from django.shortcuts import render, redirect
from userAuth.models import User
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
