from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm#, SignUpForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name','team')
    list_filter = ('email', 'first_name', 'last_name','team')
    fieldsets = (
        (None, {'fields': ('email', 'password','first_name', 'last_name', 'specialization','team')}),
        ('Разрешения', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'specialization', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'team')
    ordering = ('email', 'first_name', 'last_name', 'team') 


admin.site.register(User, CustomUserAdmin) 