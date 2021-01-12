from django.contrib import admin
from .forms import TaskAdminForm, SolutionadminForm
from .models import Task,Solution

class TaskAdmin(admin.ModelAdmin):
    add_form=TaskAdminForm
    list_display=('title', 'deadline')
    list_filter=('deadline',)
    search_fields=('title',)
    ordering=('title','deadline')

class SolutionAdmin(admin.ModelAdmin):
    add_form=SolutionadminForm
    list_display=('task','team')
    list_filter=('task',)
    search_fields=('team','task')
    ordering=('task','team')

    
admin.site.register(Task, TaskAdmin)
admin.site.register(Solution, SolutionAdmin)
# Register your models here.
