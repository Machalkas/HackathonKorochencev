from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('news/', views.listNews, name="News"),
    path('news/<key>', views.viewNews, name="viewNews"),
    path('ajax', views.manageMain, name="ajax")
]