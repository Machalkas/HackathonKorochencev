from django.contrib import admin
from .forms import CompanyForm
from .models import Company, CompanyRepresentatives

class CompanyAdmin(admin.ModelAdmin):
    add_form=CompanyForm
    list_display=('name',)
    list_filter=('name',)
    search_fields=('name',)
    ordering=('name',)

class CompanyRepresentativesAdmin(admin.ModelAdmin):
    model=CompanyRepresentatives
    list_display=('company_id', 'user_id')
    search_fields=('company_id','user_id')

    
admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyRepresentatives, CompanyRepresentativesAdmin)
# Register your models here.
