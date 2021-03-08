from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import forms
from django.contrib.auth.decorators import login_required
# from datetime import datetime
from django.utils import timezone

from .models import Task, Solution
from .forms import TaskForm, SolutionForm
from team.models import TeamsLeaders, Teams
from company.models import Company, CompanyRepresentatives
from main.models import Settings

from .checkPermissions import isAlow
months = {1:"января", 2:"февраля", 3:"марта", 4:"апреля", 5:"мая", 6:"июня", 7:"июля", 8:"августа", 9:"сентября", 10:"октября", 11:"ноября", 12:"декабря"}

def parseDateTime(dt):
    t=dt.timetuple()
    h=str(t[3])
    m=str(t[4])
    if(t[3]<10):
        h="0"+h
    if(t[4]<10):
        m="0"+m
    return str(t[2])+" "+months[t[1]]+" "+str(t[0])+" "+h+":"+m

@login_required(login_url='/auth')
def viewSolutions(request):
    is_specialist=False
    if not request.user.is_anonymous and request.user.is_specialist:
        try:
            CompanyRepresentatives.objects.get(user_id_id=request.user.pk)
        except:
            pass
        else:
            is_specialist=True
        return render(request, "tasks/view_solutions.html")
    elif not request.user.is_anonymous and request.user.is_superuser:
        is_specialist=False
        return render(request, "tasks/view_solutions.html")
    return render(request, "pages/access_denied.html")

@login_required(login_url='/auth')
def viewSolution(request, solution_pk):
    is_alow=False
    is_specialist=False
    if not request.user.is_anonymous and (request.user.is_specialist or request.user.is_superuser):
        is_alow=True
        try:
            solution=Solution.objects.get(pk=solution_pk)
            company_id=CompanyRepresentatives.objects.get(user_id_id=request.user.pk).company_id_id
        except:
            pass
        else:
            if solution.task.company.pk==company_id:
                is_specialist=True
    if not is_alow:
        return render(request, "pages/access_denied.html")
    return render(request, "tasks/view_solution.html", {"solution":solution, "is_specialist":is_specialist})

def viewTasks(request):
    if not isAlow(request):
        try:
            s=Settings.objects.all()
            now=timezone.now()
            if s[0].start_date!=None and s[0].start_date>now:
                date="Начало "+parseDateTime(s[0].start_date)
                title="Не спеши!"
                text="Хакатон еще не начался"
                return render(request, "tasks/not_in_time.html", {"title":title, "text":text, "date":date,"dt":s[0].start_date.strftime("%Y-%m-%dT%H:%M:%S")})
            elif s[0].end_date!=None and s[0].end_date<now:
                # date="Конец "+parseDateTime(s[0].start_date)
                title="Опоздал!"
                text="Хакатон закончился "+parseDateTime(s[0].end_date)
                return render(request, "tasks/not_in_time.html", {"title":title, "text":text})
        except:
            pass
    is_specialist=False
    if not request.user.is_anonymous and request.user.is_specialist:
        try:
            CompanyRepresentatives.objects.get(user_id_id=request.user.pk)
        except:
            pass
        else:
            is_specialist=True
    return render(request, "tasks/view_tasks.html",{"is_specialist":is_specialist})

def viewTask(request, task_pk):
    # if not isAlow(request):
    #     return render(request, "pages/access_denied.html")
    if request.method=="POST":
        form=SolutionForm(request.POST, request.FILES)
        #возможно излишне
        # if request.user.team==None: 
        #     return render(request, "tasks/view_task.html",{'title':'Ошибка', 'task':'Создайте команду для загрузки решения'})
        # else:
        #     try:
        #         tl=TeamsLeaders.objects.get(user_id_id=request.user.pk)
        #     except:
        #         return render(request, "tasks/view_task.html",{'title':'Ошибка', 'task':'Загружать решения может только лидер команды'})
        if form.is_valid():
            task=Task.objects.get(pk=task_pk)
            if task==request.user.team.task:
                solution=form.save()
                solution.team=request.user.team
                solution.save()
                return redirect("/tasks")
            else:
                return render(request, "tasks/view_task.html",{'title':'Ошибка', 'task':'Истек срок сдачи задания'})
        else:
            return render(request, "tasks/view_task.html",{'title':'Ошибка', 'task':form.errors})
    else:
        try:
            TeamsLeaders.objects.get(user_id=request.user.pk)
        except:
            is_leader=False
        else:
            is_leader=True
        try:
            task=Task.objects.get(pk=task_pk)
        except:
            return render(request, "tasks/view_task.html",{'title':'Ошибка', 'task':'Задание не найдено'})
        else:
            form=SolutionForm()#initial={"team":request.user.team, "task":task}
            solution=Solution.objects.filter(team=request.user.team).order_by("-created")
            return render(request, "tasks/view_task.html",{'form':form, 'pk':task.pk, 'title':task.title, 'task':task.task, 'file':task.task_file, 'company':task.company, 'is_leader':is_leader, 'solutions':solution})

@login_required(login_url='/auth')
def createTask(request):
    if request.method=="GET":
        form=TaskForm()
        return render(request, "tasks/create_task.html", {"form":form})

def manageTasks(request):
    if request.is_ajax and request.method=="POST":
        action=request.POST.get('action')
        if action=="upload-task":
            if request.user.is_anonymous or not request.user.is_specialist:
                return JsonResponse({"error":"Не достаточно прав"}, status=400)
            form=TaskForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    company_id=CompanyRepresentatives.objects.get(user_id=request.user.pk).company_id
                    company=Company.objects.get(pk=company_id)
                except:
                    return JsonResponse({"error":"Компании не существует"}, status=400)
                task=form.save()
                task.company=company
                task.save()
                return JsonResponse({"ok":task.title}, status=200)
            else:
                return JsonResponse({"error":form.errors}, status=400)
        elif action=="upload-score":
            if not request.user.is_anonymous and request.user.is_specialist:
                try:
                    s=Solution.objects.get(pk=request.POST.get("solution"))
                    s.score=int(request.POST.get("score"))
                    s.save()
                except ValueError:
                    return JsonResponse({"error":"Не верное значение"}, status=400)
                return JsonResponse({"ok":""})
            else:
                return JsonResponse({"error":"Не верный запрос"}, status=400)
            return JsonResponse({"error":"Не достаточно прав"}, status=400)

    elif request.is_ajax and request.method=="GET":
        action=request.GET.get('action')
        if action=="get-tasks":
            t=Task.objects.all()
            tasks=[]
            for i in t:
                teams=Teams.objects.filter(task=i.pk).count()
                tasks.append({'pk':i.pk, 'title':i.title, 'task':i.task, 'company':i.company.name, "teams":teams})
            return JsonResponse({"tasks":tasks})
            
        elif action=="get-solutions":
            try:
                if not request.user.is_anonymous and request.user.is_superuser:
                    task=Task.objects.all()
                else:
                    company_id=CompanyRepresentatives.objects.get(user_id_id=request.user.id).company_id_id
                    company=Company.objects.get(id=company_id)
                    task=Task.objects.filter(company=company)
                solutions_list=[]
                for i in task:
                    solutions=Solution.objects.filter(task=i.pk)
                    # s=[]
                    for j in solutions:
                        solutions_list.append({"pk":j.pk,"team":j.team.name, "task":j.task.title, "file":j.solution_file.name, "score":j.score, "max-score":i.cost, "created":j.created})
                    # solutions_list.append({"task":i.title, "solutions":s}) 
                return JsonResponse({"solutions":solutions_list}, status=200)
            except:
                return JsonResponse({"error":"Нет прав для просмотра решений"}, status=400)
        elif action=="get-solution":
            try:
                solution_id=request.GET.get('solution')
                s=Solution.objects.get(pk=solution_id)
                t=Task.objects.get(pk=s.task.pk)
                return JsonResponse({"task":t.title, "deadline":t.deadline, "task-pk":t.pk, "solution-pk":s.pk, "team":s.team.name, "file":s.solution_file.name, "upload":s.created, "max-score":t.cost, "score":s.score})
            except:
                pass
            company_id=CompanyRepresentatives.objects.get(user_id_id=request.user.id).company_id_id
            company=Company.objects.get(id=company_id)
            task=Task.objects.filter(company=company)
            for t in task:
                try:
                    s=Solution.objects.filter(task=t.pk).filter(score=None)
                    if len(s)<1:
                        continue
                except:
                    continue
                return JsonResponse({"task":t.title, "deadline":t.deadline, "task-pk":t.pk, "solution-pk":s[0].pk, "team":s[0].team.name, "file":s[0].solution_file.name, "upload":s[0].created, "max-score":t.cost, "score":None})
            return JsonResponse({"url":"/tasks/solutions"})
        else:
            return JsonResponse({"error":""}, status=400)
    else:
        return HttpResponse("Не поддерживаемый запрос")

# Create your views here.
 