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

class CheckpointAdmin(admin.ModelAdmin):
    model=Checkpoint
    list_display=('title', 'start_date','end_date')
    # list_filter=('score',)

class NewsAdmin(admin.ModelAdmin):
    model=News
    list_display=('title', 'created')
    # list_filter=('score',)

admin.site.register(Settings, SettingsAdmin)
admin.site.register(Checkpoint, CheckpointAdmin)
admin.site.register(Rating)
admin.site.register(News, NewsAdmin)
# Register your models here.
