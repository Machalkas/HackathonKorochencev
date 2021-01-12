from django import forms
from .models import Task, Solution

class TaskForm(forms.ModelForm):
    title=forms.CharField(max_length=100, label="Заголовок")
    task=forms.CharField(label="Задание")
    task_file=forms.FileField(required=False, label="Файл задания")
    cost=forms.IntegerField(label="Максимальный балл за задание")
    deadline=forms.DateTimeField(label="Дедлайн")
    class Meta:
        model=Task
        fields=('title', 'task', 'task_file', 'cost', 'deadline')

class TaskAdminForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=('title', 'task', 'task_file', 'cost', 'deadline')


class Solutionform(forms.ModelForm):
    solution=forms.CharField(label="Решение")
    solution_file=forms.FileField(required=False, label="Файл решения")
    score=forms.IntegerField(required=False, label="Баллы за задание")
    class Meta:
        model=Solution
        fields=('solution', 'solution_file')

class SolutionadminForm(forms.ModelForm):
    class Meta:
        model=Solution
        fields=('team', 'task', 'solution', 'solution_file', 'score')