from django.contrib import admin
from .models import Settings

class SettingsAdmin(admin.ModelAdmin):
    model=Settings
    list_display=('start_date', 'end_date','max_teams','max_members')
    # list_filter=('score',)
    fieldsets=(
        (None,{'fields':('start_date', 'end_date','max_teams','max_members')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':('start_date', 'end_date','max_teams','max_members')}
        ),
    )


admin.site.register(Settings, SettingsAdmin)
# Register your models here.
