from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Teams, TeamsLeaders
from .forms import CreateTeamForm
from userAuth.models import User
from .urlGenerator import generate
# from django.contrib.auth.models import User

def generateValidator():
    count=0
    size=10
    while True:
        count+=1
        if count>50:
            size+=1
        print(size)
        s=generate(size=size)
        try:
            t=Teams.objects.get(url=s)
        except:
            return s

@login_required(login_url='/auth/login')
def viewTeam(request):
    if(request.user.team==None):
        return render(request, "not_exist.html")
    team_pk=request.user.team.id
    team=Teams.objects.get(id=team_pk)
    lider_id=TeamsLeaders.objects.get(team_id=team_pk).user_id_id
    members=[]
    for i in User.objects.filter(team=team_pk):
        members.append(i)
    return render(request, "view_team.html",{'team_name':team.name, 'discription':team.description,'link':team.link , 'url':request.META['HTTP_HOST']+'/team/invite/'+team.url, 'score':team.score, 'lider_id':lider_id, 'members':members})

@login_required(login_url='/auth/login')
def createTeam(request):
    if request.user.team==None:
        if request.method=="POST":
            form = CreateTeamForm(request.POST)
            if form.is_valid():
                team=form.save()
                team.url=generateValidator()
                id_team=Teams.objects.get(id=team.id)
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
def addMember(request,key):
        if request.method=='POST':
            team_id=request.POST.get('team_id')
            team_id=Teams.objects.get(name=team_id)
            user=User.objects.get(pk=request.user.pk)
            user.team=team_id
            user.save()
            return redirect("/team/view")
        else:
            team=Teams.objects.get(url=key)
            return render(request,"invite.html",{'team':team.name})

def manageTeam(request):
    if request.method=="POST":
        team=request.POST.get('team')
        disc=request.POST.get('disc')
        link=request.POST.get('link')
        print(team)
        print(disc)
        print(link)
        return HttpResponse("Ok")
def getScore(request):
    if request.method=="GET":
        try:
            team=request.GET.get('team')
            team=Teams.objects.get(pk=team)
            return HttpResponse(team.score)
        except:
            return HttpResponse("None")
    else:
        return HttpResponse(request,'only GET')

# Create your views here.
