from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from .models import Teams, TeamsLeaders
from .forms import CreateTeamForm
from userAuth.models import User
from .urlGenerator import generate
from tasks.models import Solution
from main.models import Settings

# from django.contrib.auth.models import User

def generateValidator():
    count=0
    size=10
    while True:
        count+=1
        if count>50:
            size+=1
        # print(size)
        s=generate(size=size)
        try:
            t=Teams.objects.get(url=s)
        except:
            return s
def isFullOfTeams():
    try:
        s=Settings.objects.all()[0].max_teams
        t=Teams.objects.all().count()
        if s!=None and t>=s:
            return True
    except:
        pass
    return False
def isFullOfMembers(team_url):
    try:
        t=Teams.objects.get(url=team_url).pk
        s=Settings.objects.all()[0].max_members
        m=User.objects.filter(team=t).count()
        if s!=None and m>=s:
            return True
    except:
        pass
    return False

def viewTeams(request):
    return render(request, "view_teams.html")

# @login_required(login_url='/auth')
def viewTeam(request, key=None):
    if key!=None:
        try:
            team_pk=Teams.objects.get(name=key).pk
        except:
            return redirect("/team")
    else:
        if(request.user.team==None):
            return render(request, "not_exist.html")
        team_pk=request.user.team.id
    team=Teams.objects.get(id=team_pk)
    lider_id=TeamsLeaders.objects.get(team_id=team_pk).user_id_id
    members=[]
    for i in User.objects.filter(team=team_pk):
        members.append(i)
    form=CreateTeamForm()
    s=Solution.objects.filter(team=team)
    score=0
    try:
        for i in s:
            score+=i.score
    except:
        pass
    return render(request, "view_team.html",{'team_pk':team.pk,'team_name':team.name, 'link':team.link , 'url':request.META['HTTP_HOST']+'/team/invite/'+team.url, 'score':score, 'lider_id':lider_id, 'members':members, 'form':form}) # 'discription':team.description.replace("\r","[[r]]").replace("\n","[[n]]"),

@login_required(login_url='/auth')
def sendForm(request):
    if isFullOfTeams():
        return render(request, "full.html", {"full_text":"Лимит количества команд превышен"})
    if request.user.team==None:
        if request.method=="GET":
            form=CreateTeamForm()
            return render(request, "create_team.html", {'form':form})
    return redirect("/team")

@login_required(login_url='/auth')
def addMember(request,key):
    if isFullOfMembers(key):
        return render(request, "full.html", {"full_text":"Лимит количества участников в одной команде превышен"})
    if request.method=='POST':
        team_id=request.POST.get('team_id')
        team_id=Teams.objects.get(name=team_id)
        user=User.objects.get(pk=request.user.pk)
        user.team=team_id
        user.save()
        return redirect("/team")
    else:
        team=Teams.objects.get(url=key)
        return render(request,"invite.html",{'team':team.name})

def manageTeam(request):
    if request.is_ajax and request.method == "POST":
        action=request.POST.get('action')
        print(checkPermissions(request))
        if action=='delete-member':
            if checkPermissions(request)[0]!=True and checkPermissions(request)[1]!=True:
                return JsonResponse({"error":"Недостаточно прав для выполнения запроса"}, status=400)
            errors=""
            leader=TeamsLeaders.objects.get(team_id=request.user.team)
            user_pk=request.POST.get("member")
            if user_pk!=None:
                user=User.objects.get(pk=user_pk)
                if leader.user_id_id==int(user_pk):
                    errors+="Нельзя удалить пользователя "+user.email+" т.к. он является лидером команды\n"
                else:
                    user.team=None
                    user.save()
            if errors!='':
                return JsonResponse({"error":errors}, status=400)
            return JsonResponse({"ok":""}, status=200)
        elif action=="create-team":
            if isFullOfTeams():
                return JsonResponse({"error":"Лимит количества команд превышен"}, status=400)
            form = CreateTeamForm(request.POST)
            if form.is_valid():
                team=form.save()
                team.url=generateValidator()
                id_team=Teams.objects.get(id=team.id)
                user=User.objects.get(pk=request.user.pk)
                user.team=id_team
                tl=TeamsLeaders(user_id=user, team_id=id_team)
                tl.save()
                user.save()
                team.save()
                return JsonResponse({"url":"/team/"}, status=200)
            else:
                return JsonResponse({"error":form.errors}, status=400)
        elif checkPermissions(request)[0]!=True:#повышение прав доступа
                return JsonResponse({"error":"Недостаточно прав для выполнения запроса "+action}, status=400)
        elif action=='update':
            team=Teams.objects.get(id=request.user.team.id)
            form=CreateTeamForm(request.POST, instance=team)
            url=team.url
            if form.is_valid():
                team.url=url
                team.save()
                return JsonResponse({'data':{'name':team.name, 'link':team.link}},status=200)
            else:
                return JsonResponse({'error':form.errors}, status=400)   
        elif action=='update-members':
            status=[{"change-leader":None, "delete-members":None},200]
            if request.POST.get('leader')!='':
                try:
                    leader=TeamsLeaders.objects.get(team_id=request.POST.get('team'))
                except:
                    status[0]["change-leader"]={"error":"Группа "+request.POST.get('team')+" не найдена"}
                    status[1]=400
                else:
                    try:
                        user=User.objects.get(pk=request.POST.get('leader'))
                    except:
                        status[0]["change-leader"]={"error":"Лидер "+request.POST.get('leader')+" не найден"}
                        status[1]=400
                    else:  
                        if user.team.pk==int(request.POST.get('team')):
                            leader.user_id_id=user.pk
                            leader.save()
                            status[0]["change-leader"]={"ok":""}
                        else:
                            status[0]["change-leader"]={"error":"Пользователь "+user.email+" не состаит в группе "+request.POST.get('team')}
                            status[1]=400
            else:
                status[0]["change-leader"]={"ok":""}
            i=0#удаление пользователя
            leader=TeamsLeaders.objects.get(team_id=request.user.team)
            errors=''
            while True:
                user_pk=request.POST.get("delete-members["+str(i)+"]")
                if user_pk==None:
                    break
                user=User.objects.get(pk=user_pk)
                if leader.user_id_id==int(user_pk):
                    errors+="Нельзя удалить пользователя "+user.email+" т.к. он является лидером команды\n"
                else:
                    user.team=None
                    user.save()
                i+=1
            if errors!='':
                status[0]["delete-members"]={"error":errors}
                status[1]=400
            else:
                status[0]["delete-members"]={"ok":""}
            return JsonResponse(status[0],status=status[1])
        else:
            return JsonResponse({"error":"Новозможно обработать запрос "+action},status=400)
    elif request.is_ajax and request.method=='GET':#GET
        if request.GET.get('action')=='request':
            team=request.GET.get('team')
            team=Teams.objects.get(pk=team)
            members=User.objects.filter(team=team)
            leader=TeamsLeaders.objects.get(team_id=team.pk)
            # print(members[0].first_name)
            m=[]
            for i in members:
                is_lider=False
                if leader.user_id_id==i.pk:
                    is_lider=True
                m.append({'id':i.pk,'first_name':i.first_name, 'last_name':i.last_name, 'email':i.email, 'specialization':i.specialization, 'is_lider':is_lider})
            s=Solution.objects.filter(team=team)
            score=0
            try:
                for i in s:
                    score+=i.score
            except:
                pass
            return JsonResponse({'score':score,'members':m})
        elif request.GET.get('action')=="get-teams":
            teams=[]
            t=Teams.objects.all()#.order_by("-score")
            for i in t:
                s=Solution.objects.filter(team=i)
                score=0
                try:
                    for j in s:
                        score+=j.score
                except:
                    pass
                teams.append({"pk":i.pk, "name":i.name, "score":score})
            # teams=sorted(teams, key=lambda team:team["score"], reverse=True)
            return JsonResponse({'teams':teams}) 
        else:
            return JsonResponse({"error":""},status=400)
    return HttpResponse(request, 'only for AJAX')

def checkPermissions(request):
    try:
        leader=TeamsLeaders.objects.get(team_id=request.user.team)
    except:
        return [None,None]
    status=[False,False]
    if request.POST.get("member")!=None:
        status[1]=int(request.POST.get("member"))==request.user.pk
    status[0]=request.user.pk==leader.user_id_id
    print(status)
    return status

def getScore(request):
    if request.method=="GET":
        try:
            team=request.GET.get('team')
            team=Teams.objects.get(name=team)
            return HttpResponse(team.score)
        except:
            return HttpResponse("None")
    else:
        return HttpResponse(request,'only GET')
# Create your views here.  