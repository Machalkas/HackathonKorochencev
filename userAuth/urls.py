from django.urls import path
from . import views

urlpatterns = [
    path('join', views.join, name="index"),
    path('login', views.user_login, name="index"),
    path('logout', views.user_logout, name="index"),
]