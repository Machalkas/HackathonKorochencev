from django.urls import path
from . import views

urlpatterns=[
    path('', views.viewCompanies, name="view-companies"),
    path('view/<key>', views.viewCompany, name="view-company"),
    path('create', views.createCompany, name="create-company"),
    path('managecompany', views.manageCompany, name="managecompany"),
]