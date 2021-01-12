from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone

from .models import Task, Solution
from .forms import TaskForm, Solutionform

def viewTasks(request):
    return render(request, "view_tasks.html")


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
                    active.append({'title':i.title, 'task':i.task, 'cost':i.cost, 'deadline':i.deadline})
                else:
                    completed.append({'title':i.title, 'task':i.task, 'cost':i.cost, 'deadline':i.deadline})
            return JsonResponse({'active':active, 'complited':completed})

            
    else:
        return HttpResponse("Не поддерживаемый запрос")

# Create your views here.
