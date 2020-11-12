from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Teams, TeamsLeaders
from .forms import CreateTeamForm
from userAuth.models import User
# from django.contrib.auth.models import User

@login_required(login_url='/auth/login')
def viewTeam(request):
    if(request.user.team==None):
        return render(request, "not_exist.html")
    return render(request, "view_team.html")

def createTeam(request):
    if request.user.team==None:
        if request.method=="POST":
            form = CreateTeamForm(request.POST)
            if form.is_valid():
                team=form.save()
                team.save()
                id_team=Teams.objects.get(name=form.cleaned_data.get('name'))
                user=User.objects.get(pk=request.user.pk)
                user.team=id_team
                user.save()
                # tl=TeamsLeaders.objects.all()
                # tl=TeamsLeaders
                # tl.user_id=user.pk
                # tl.team_id=id_team
                tl=TeamsLeaders(user_id=user, team_id=id_team)
                tl.save()
                return redirect("/team/view")
        else:
            form=CreateTeamForm()
        return render(request, "create_team.html", {'form':form})
    else:
        return redirect("/team/view")
# Create your views here.
