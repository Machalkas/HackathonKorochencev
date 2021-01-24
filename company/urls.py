from django.urls import path
from . import views

urlpatterns=[
    path('', views.viewCompany, name="view-company"),
    path('create', views.createCompany, name="create-company"),
]