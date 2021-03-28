from django.urls import path
from . import views

urlpatterns = [
    path('',views.viewTasks, name="view-tasks"),
    path('view/<task_pk>', views.viewTask, name="view-task"),
    path('create/', views.createTask, name="create-task"),
    # path('solutions/', views.viewSolutions, name="view_solutions"),
    #  path('solutions/view/<solution_pk>', views.viewSolution, name="view_solution"),
    path('managetasks', views.manageTasks, name="manage-tasks"),
]