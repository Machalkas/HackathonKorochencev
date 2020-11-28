from django.urls import path
from . import views

urlpatterns = [
    path('view', views.viewTeam, name="view-team"),
    path('create', views.createTeam, name="create-team"),
    path('invite/<key>/',views.addMember, name="invite")
]