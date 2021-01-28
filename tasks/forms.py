from django import forms
from .models import Task, Solution
from team.models import Teams

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
    # solution=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control mt-1', 'placeholder':'Решение'}))
    solution_file=forms.FileField(required=True, label="Файл решения")
    task=forms.ModelChoiceField(widget=forms.HiddenInput(), queryset = Task.objects.all(), required = False)
    team=forms.ModelChoiceField(widget=forms.HiddenInput(), queryset = Teams.objects.all(), required = False)
    class Meta:
        model=Solution
        fields=('solution_file','task','team')

class SolutionadminForm(forms.ModelForm):
    class Meta:
        model=Solution
        fields=('team', 'task', 'solution_file', 'score')