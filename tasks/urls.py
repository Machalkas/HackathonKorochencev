from django.urls import path
from . import views

urlpatterns = [
    path('',views.viewTasks, name="view-tasks"),
    # path('/<key>/', views.viewTask, name="view-task"),
    # path('create-task', views.createTask, name="create-task"),
    # path('create-solution',views.createSolution, name="create-solution"),
]