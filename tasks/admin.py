from django.contrib import admin
from .forms import TaskAdminForm, SolutionadminForm
from .models import Task,Solution

class TaskAdmin(admin.ModelAdmin):
    add_form=TaskAdminForm
    list_display=('title', 'created', 'company')
    search_fields=('title', 'company')
    ordering=('title','created')

class SolutionAdmin(admin.ModelAdmin):
    add_form=SolutionadminForm
    list_display=('team', 'created')
    list_filter=('team',)
    search_fields=('team',)
    ordering=('team', 'created')

    
admin.site.register(Task, TaskAdmin)
admin.site.register(Solution, SolutionAdmin)
# Register your models here.
