from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm#, SignUpForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name','team','is_specialist','is_superuser')
    list_filter = ('specialization','team','is_specialist')
    fieldsets = (
        (None, {'fields': ('email', 'password',('first_name', 'last_name'), 'specialization','team')}),
        ('Разрешения', {'fields': ('is_specialist','is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'specialization', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'team')
    ordering = ('email','team') 
    # def delete_model(self, request, queryset):
    #     for obj in queryset:
    #         print(obj)
    #         obj.delete()
    # actions=[delete_model]


admin.site.register(User, CustomUserAdmin)