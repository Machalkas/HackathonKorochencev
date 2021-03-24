from django.contrib import admin
from .models import Settings, Checkpoint, Rating, News

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
admin.site.register(Checkpoint)
admin.site.register(Rating)
admin.site.register(News)
# Register your models here.
