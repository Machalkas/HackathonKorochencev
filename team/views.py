from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Teams, TeamsLeaders
from .forms import CreateTeamForm
from userAuth.models import User
from .urlGenerator import generate
# from django.contrib.auth.models import User

def generateValidator():
    while True:
        s=generate()
        try:
            t=Teams.objects.get(url=s)
        except:
            return s

@login_required(login_url='/auth/login')
def viewTeam(request):
    if(request.user.team==None):
        return render(request, "not_exist.html")
    team_pk=request.user.team.pk
    team=Teams.objects.get(pk=team_pk)
    lider_id=TeamsLeaders.objects.get(team_id=team_pk).user_id_id
    members=[]
    for i in User.objects.filter(team=team_pk):
        members.append(i)
    return render(request, "view_team.html",{'team_name':team.name, 'discription':team.description, 'url':team.url, 'lider_id':lider_id, 'members':members})

@login_required(login_url='/auth/login')
def createTeam(request):
    if request.user.team==None:
        if request.method=="POST":
            form = CreateTeamForm(request.POST)
            if form.is_valid():
                team=form.save()
                team.url=generateValidator()
                id_team=Teams.objects.get(name=form.cleaned_data.get('name'))
                user=User.objects.get(pk=request.user.pk)
                user.team=id_team
                # tl=TeamsLeaders.objects.all()
                # tl=TeamsLeaders
                # tl.user_id=user.pk
                # tl.team_id=id_team
                tl=TeamsLeaders(user_id=user, team_id=id_team)
                tl.save()
                user.save()
                team.save()
                return redirect("/team/view")
        else:
            form=CreateTeamForm()
        return render(request, "create_team.html", {'form':form})
    else:
        return redirect("/team/view")

@login_required(login_url='/auth/login')
def addMember(request):
    pass
# Create your views here.
