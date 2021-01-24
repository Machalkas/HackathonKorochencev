from django.urls import path
from . import views

urlpatterns = [
    path('', views.viewTeam, name="view-team"),
    path('create', views.sendForm, name="create-team"),
    path('invite/<key>/',views.addMember, name="invite"),
    path('score',views.getScore, name="getScore"),
    path('ajax',views.manageTeam, name="manageTeam"),
]