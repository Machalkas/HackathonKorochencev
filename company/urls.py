from django.urls import path
from . import views

urlpatterns=[
    path('', views.viewCompanies, name="view-company"),
    path('create', views.createCompany, name="create-company"),
    path('managecompany', views.manageCompany, name="create-company"),
]