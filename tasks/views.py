from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import forms
# from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone

from .models import Task, Solution
from .forms import TaskForm, SolutionForm

from team.models import TeamsLeaders

def viewTasks(request):
    return render(request, "tasks/view_tasks.html")

def viewTask(request, task_pk):
    months = {0:"января", 1:"февраля", 2:"марта", 3:"апреля", 4:"мая", 5:"июня", 6:"июля", 7:"августа", 8:"сентября", 9:"октября", 10:"ноября", 11:"декабря"}
    if request.method=="POST":
        form=SolutionForm(request.POST, request.FILES)
        if form.is_valid():
            now = timezone.now()
            solution=form.save()
            solution.task=Task.objects.get(pk=task_pk)
            solution.team=request.user.team
            solution.save()
            return redirect("/tasks")
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

def createTask(request):
    if request.method=="GET":
        form=TaskForm()
        return render(request, "tasks/create_task.html", {"form":form})

def manageTasks(request):
    if request.is_ajax and request.method=="POST":
        pass
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
    else:
        return HttpResponse("Не поддерживаемый запрос")

# Create your views here.
