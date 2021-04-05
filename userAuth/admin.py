from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm#, SignUpForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    # readonly_fields=("reset_token",)
    list_display = ('email', 'first_name', 'last_name','team','is_specialist','is_superuser', 'is_auditor')
    list_filter = ('specialization','team','is_specialist', 'is_auditor')
    fieldsets = (
        (None, {'fields': ('email', 'password',('first_name', 'last_name'), 'specialization','team', 'reset_token')}),
        ('Разрешения', {'fields': ('is_specialist','is_auditor','is_staff','is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'specialization', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email','team') 
    # def delete_model(self, request, queryset):
    #     for obj in queryset:
    #         print(obj)
    #         obj.delete()
    # actions=[delete_model]


admin.site.register(User, CustomUserAdmin)