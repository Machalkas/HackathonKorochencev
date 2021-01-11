from django.contrib import admin
from .forms import TeamsAdminForm
from .models import Teams, TeamsLeaders

class TeamsAdmin(admin.ModelAdmin):
    add_form=TeamsAdminForm
    model=Teams
    list_display=('name','score')
    list_filter=('score',)
    fieldsets=(
        (None,{'fields':('name','description','score','link','url')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':('name','description','link')}
        ),
    )
    search_fields=('name',)
    ordering=('name','link')

class TeamsLeadersAdmin(admin.ModelAdmin):
    model=TeamsLeaders
    list_display=('team_id', 'user_id')
    search_fields=('team_id','user_id')

admin.site.register(Teams, TeamsAdmin)
admin.site.register(TeamsLeaders, TeamsLeadersAdmin)
# Register your models here.
