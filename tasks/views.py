from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone

from .models import Task, Solution
from .forms import TaskForm, SolutionForm

from team.models import TeamsLeaders

def viewTasks(request):
    return render(request, "view_tasks.html")

def viewTask(request, task_pk):
    months = {0:"января", 1:"февраля", 2:"марта", 3:"апреля", 4:"мая", 5:"июня", 6:"июля", 7:"августа", 8:"сентября", 9:"октября", 10:"ноября", 11:"декабря"}
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
        return render(request, "view_task.html",{'title':'Ошибка', 'task':'Задание не найдено'})
    else:
        form=SolutionForm()
        return render(request, "view_task.html",{'form':form, 'title':task.title, 'task':task.task, "deadline":deadline, 'is_leader':is_leader})

def createSolution(request, task_pk):
    task=Task.objects.get(pk=task_pk)
    if request.method=="POST":
        form=SolutionForm(request.POST, request.FILES)
        if form.is_valid():
            solution=form.save()
            solution.save()
            redirect('tasks')     
    else:
        form=SolutionForm()
    return render(request, "create_solution.html",{"form":form,'task':task.task})

def manageTasks(request):
    if request.is_ajax and request.method=="POST":
        pass
    elif request.is_ajax and request.method=="GET":
        if request.GET.get('action')=="get-tasks":
            now = timezone.now()
            active=[]
            completed=[]
            tasks=Task.objects.all()
            for i in tasks:
                if i.deadline>now:
                    active.append({'pk':i.pk, 'title':i.title, 'task':i.task, 'cost':i.cost, 'deadline':i.deadline})
                else:
                    completed.append({'pk':i.pk, 'title':i.title, 'task':i.task, 'cost':i.cost, 'deadline':i.deadline})
            return JsonResponse({'active':active, 'complited':completed})

            
    else:
        return HttpResponse("Не поддерживаемый запрос")

# Create your views here.
