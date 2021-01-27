from django.urls import path
from . import views

urlpatterns = [
    path('',views.viewTasks, name="view-tasks"),
    path('<task_pk>/', views.viewTask, name="view-task"),
    # path('create-task', views.createTask, name="create-task"),
    # path('<task_pk>/create-solution',views.createSolution, name="create-solution"),
    path('managetasks', views.manageTasks, name="manage-tasks"),
]