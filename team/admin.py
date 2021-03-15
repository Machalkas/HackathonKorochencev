from django.contrib import admin
from .forms import TeamsAdminForm
from .models import Teams, TeamsLeaders, Checked

class TeamsAdmin(admin.ModelAdmin):
    add_form=TeamsAdminForm
    model=Teams
    list_display=('name','task')
    # list_filter=('score',)
    # fieldsets=(
    #     (None,{'fields':('name','link','url')}),
    # )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':('name','link')}
        ),
    )
    search_fields=('name','task')
    ordering=('name','task')

class TeamsLeadersAdmin(admin.ModelAdmin):
    model=TeamsLeaders
    list_display=('team_id', 'user_id')
    search_fields=('team_id','user_id')

class CheckedAdmin(admin.ModelAdmin):
    model=Checked
    list_display=('team', 'checkpoint', 'is_came')
    search_fields=['team__name']
    list_filter=('checkpoint','is_came')


admin.site.register(Teams, TeamsAdmin)
admin.site.register(TeamsLeaders, TeamsLeadersAdmin)
admin.site.register(Checked, CheckedAdmin)
# Register your models here.
