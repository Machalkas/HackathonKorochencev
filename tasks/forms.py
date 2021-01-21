from django import forms
from .models import Task, Solution

class TaskForm(forms.ModelForm):
    title=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control mt-1', 'placeholder':'Заголовок'}))
    task=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mt-1', 'placeholder':'Задание'}))
    task_file=forms.FileField(required=False, widget=forms.TextInput(attrs={'class':'form-control mt-1', 'placeholder':'Файл задания'}))
    cost=forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control mt-1', 'placeholder':'Баллы за задание'}))
    deadline=forms.DateTimeField(widget=forms.TextInput(attrs={'class':'form-control mt-1', 'placeholder':'Дедлайн'}))
    class Meta:
        model=Task
        fields=('title', 'task', 'task_file', 'cost', 'deadline')

class TaskAdminForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=('title', 'task', 'task_file', 'cost', 'deadline')


class SolutionForm(forms.ModelForm):
    solution=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control mt-1', 'placeholder':'Решение'}))
    solution_file=forms.FileField(required=False, label="Файл решения")
    class Meta:
        model=Solution
        fields=('solution', 'solution_file')

class SolutionadminForm(forms.ModelForm):
    class Meta:
        model=Solution
        fields=('team', 'task', 'solution', 'solution_file', 'score')