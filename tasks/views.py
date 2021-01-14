from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone

from .models import Task, Solution
from .forms import TaskForm, Solutionform

def viewTasks(request):
    return render(request, "view_tasks.html")

def viewTask(request, key):
    try:
        task=Task.objects.get(pk=key)
    except:
        return render(request, "view_task.html",{'title':'Ошибка', 'task':'Задание не найдено'})
    else:
        return render(request, "view_task.html",{'title':task.title, 'task':task.task})


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
