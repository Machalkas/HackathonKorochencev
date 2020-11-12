from django.urls import path
from . import views

urlpatterns = [
    path('view', views.viewTeam, name="view team"),
    path('create', views.createTeam, name="create team")
]