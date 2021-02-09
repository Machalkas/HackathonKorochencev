from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import forms
# from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone

from .models import Task, Solution
from .forms import TaskForm, SolutionForm
from team.models import TeamsLeaders
from company.models import Company, CompanyRepresentatives

def viewTasks(request):
    is_specialist=False
    if request.user.is_specialist:
        try:
            CompanyRepresentatives.objects.get(user_id_id=request.user.pk)
        except:
            pass
        else:
            is_specialist=True
    return render(request, "tasks/view_tasks.html",{"is_specialist":is_specialist})

def viewSolutions(request):
    return render(request, "tasks/view_solutions.html")

def viewTask(request, task_pk):
    months = {0:"января", 1:"февраля", 2:"марта", 3:"апреля", 4:"мая", 5:"июня", 6:"июля", 7:"августа", 8:"сентября", 9:"октября", 10:"ноября", 11:"декабря"}
    if request.method=="POST":
        form=SolutionForm(request.POST, request.FILES)
        if form.is_valid():
            now = timezone.now()
            task=Task.objects.get(pk=task_pk)
            if task.deadline>=now:
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
            t=task.deadline.timetuple()
            h=str(t[3])
            m=str(t[4])
            if(t[3]<10):
                h="0"+h
            if(t[4]<10):
                m="0"+m
            deadline=str(t[2])+" "+months[t[1]]+" "+str(t[0])+" "+h+":"+m
        except:
            return render(request, "tasks/view_task.html",{'title':'Ошибка', 'task':'Задание не найдено'})
        else:
            form=SolutionForm()#initial={"team":request.user.team, "task":task}
            now = timezone.now()
            is_active=False
            if task.deadline>=now:
                is_active=True
            return render(request, "tasks/view_task.html",{'form':form, 'title':task.title, 'task':task.task, 'file':task.task_file, 'company':task.company, "deadline":deadline, 'is_leader':is_leader, "is_active":is_active})

def viewSolution(request, solution_pk):
    return HttpResponse(solution_pk)

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
                if i.deadline>=now:
                    active.append({'pk':i.pk, 'title':i.title, 'task':i.task, 'cost':i.cost, 'deadline':i.deadline, 'company':i.company.name})
                else:
                    completed.append({'pk':i.pk, 'title':i.title, 'task':i.task, 'cost':i.cost, 'deadline':i.deadline, 'company':i.company.name})
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
        else:
            return JsonResponse({"error":""}, status=400)
    else:
        return HttpResponse("Не поддерживаемый запрос")

# Create your views here.
 