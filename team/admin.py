from django.contrib import admin
from .forms import AdminPanel
from .models import Teams, TeamsLeaders

class TeamsAdmin(admin.ModelAdmin):
    # form=AdminPanel
    model=Teams
    list_display=('name','score')
    list_filter=('name',)
    fieldsets=(
        (None,{'fields':('name','description','score','link','url')}),
    )
    add_fields=(
        (None,{'fields':('name','description','link')})
    )
    search_fields=('name',)
    ordering=('name','link')
admin.site.register(Teams, TeamsAdmin)
# admin.site.register(TeamsLeaders)
# Register your models here.
