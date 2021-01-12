from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import Task, Solution
from .forms import TaskForm, Solutionform

def viewTasks(request):
    tasks=Task.objects.all()
    return render(request, "view_tasks.html",{"tasks":tasks})

# Create your views here.
