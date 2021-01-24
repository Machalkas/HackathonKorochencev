from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from userAuth.models import User
from .forms import CompanyForm
from .models import CompanyRepresentatives, Company
from django.http import HttpResponse


@login_required(login_url='/auth')
def viewCompany(request):
    try:
        company_id=CompanyRepresentatives.objects.get(user_id_id=request.user.pk).company_id_id
        company=Company.objects.get(pk=company_id)
        representatives_id=CompanyRepresentatives.objects.filter(company_id_id=company_id)
        representatives=[]
        for i in representatives_id:
            representatives.append(User.objects.get(pk=i.user_id_id))
    except:
        return render(request, "company_not_exist.html")
    return render(request, "view_company.html", {'company':company, 'rep':representatives})


@login_required(login_url='/auth')
def createCompany(request):
    if request.method=="POST":
        form=CompanyForm(request.POST)
        if form.is_valid():
            user=User.objects.get(pk=request.user.pk)
            company=form.save()
            cr=CompanyRepresentatives(user_id=user, company_id=company)
            cr.save()
            company.save()
            return redirect("/company/view")
    else:
        form=CompanyForm()
    return render(request, "create_company.html", {"form":form})

