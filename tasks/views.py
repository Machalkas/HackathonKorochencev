from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import forms
# from django.contrib.auth.decorators import login_required
# from datetime import datetime
from django.utils import timezone

from .models import Task, Solution
from .forms import TaskForm, SolutionForm
from team.models import TeamsLeaders
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

def viewSolutions(request):
    is_specialist=False
    if request.user.is_specialist:
        try:
            CompanyRepresentatives.objects.get(user_id_id=request.user.pk)
        except:
            pass
        else:
            is_specialist=True
    return render(request, "tasks/view_solutions.html")

def viewSolution(request, solution_pk):
    is_alow=False
    if request.user.is_specialist:
        try:
            company_id=CompanyRepresentatives.objects.get(user_id_id=request.user.pk).company_id_id
            solution=Solution.objects.get(pk=solution_pk)
        except:
            pass
        else:
            if solution.task.company.pk==company_id:
                is_alow=True
    if not is_alow:
        return render(request, "tasks/access_denied.html")
    return render(request, "tasks/view_solution.html", {"solution":solution})

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
    if not isAlow(request):
        return render(request, "tasks/access_denied.html")
    if request.method=="POST":
        form=SolutionForm(request.POST, request.FILES)
        if form.is_valid():
            now = timezone.now()
            task=Task.objects.get(pk=task_pk)
            if task.deadline>=now:
                try:
                    solution=Solution.objects.get(team=request.user.team, task=task)
                    solution.solution_file=form.cleaned_data["solution_file"]
                    solution.score=None
                except:
                    solution=form.save()
                    solution.task=task
                    solution.team=request.user.team
                solution.save()
                return redirect("/tasks")
            else:
                return render(request, "tasks/view_task.html",{'title':'Ошибка', 'task':'Истек срок сдачи задания'})
    else:
        try:
            TeamsLeaders.objects.get(user_id=request.user.pk)
        except:
            is_leader=False
        else:
            is_leader=True
        try:
            task=Task.objects.get(pk=task_pk)
            deadline=parseDateTime(task.deadline)
        except:
            return render(request, "tasks/view_task.html",{'title':'Ошибка', 'task':'Задание не найдено'})
        else:
            form=SolutionForm()#initial={"team":request.user.team, "task":task}
            now = timezone.now()
            is_active=False
            if task.deadline>=now:
                is_active=True
            task_status=None
            solution_score=0
            try:
                 s=Solution.objects.get(task=task.pk, team=request.user.team)
            except:
                pass
            else:
                if s.score==None:
                    task_status="uploaded"
                else:
                    solution_score=s.score
                    task_status="checked"
            return render(request, "tasks/view_task.html",{'form':form, 'title':task.title, 'task':task.task, 'file':task.task_file, 'company':task.company, "deadline":deadline, 'is_leader':is_leader, "is_active":is_active, "task_status":task_status, "cost":task.cost, "score":solution_score})

def createTask(request):
    if request.method=="GET":
        form=TaskForm()
        return render(request, "tasks/create_task.html", {"form":form})

def manageTasks(request):
    if request.is_ajax and request.method=="POST":
        action=request.POST.get('action')
        if action=="upload-task":
            form=TaskForm(request.POST, request.FILES)
            if form.is_valid():
                company_id=CompanyRepresentatives.objects.get(user_id_id=request.user.pk).company_id_id
                company=Company.objects.get(pk=company_id)
                task=form.save()
                task.company=company
                task.save()
                return JsonResponse({"ok":task.title}, status=200)
            else:
                return JsonResponse({"error":form.errors}, status=400)
        elif action=="upload-score":
            try:
                s=Solution.objects.get(pk=request.POST.get("solution"))
                s.score=int(request.POST.get("score"))
                s.save()
            except ValueError:
                return JsonResponse({"error":"Не верное значение"}, status=400)
            return JsonResponse({"ok":""})
        else:
            return JsonResponse({"error":"Не верный запрос"}, status=400)

    elif request.is_ajax and request.method=="GET":
        action=request.GET.get('action')
        if action=="get-tasks":
            now = timezone.now()
            active=[]
            completed=[]
            tasks=Task.objects.all()
            for i in tasks:
                task_status=None
                solution_score=0
                try:
                    s=Solution.objects.get(task=i.pk, team=request.user.team)
                    if s.score!=None:
                        solution_score=s.score
                        task_status='checked'
                    else:
                        task_status='uploaded'
                except:
                    pass
                if i.deadline>=now:
                    active.append({'pk':i.pk, 'title':i.title, 'task':i.task, 'deadline':i.deadline, 'company':i.company.name, 'task-status':task_status, 'score':solution_score, 'cost':i.cost})
                else:
                    completed.append({'pk':i.pk, 'title':i.title, 'task':i.task, 'deadline':i.deadline, 'company':i.company.name, 'task-status':task_status, 'score':solution_score, 'cost':i.cost})
            return JsonResponse({'active':active, 'complited':completed})
        elif action=="get-solutions":
            try:
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
 