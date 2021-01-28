from django.db import models
from team.models import Teams
from company.models import Company
from datetime import datetime

# def setTaskDirecrory(instanse, file):
#     return 'tasks/{1}/{2}'.format(instanse.user)
# def setSolutionDirecrory(instanse, file):
#     return 'solution/{1}/{2}'.format(instanse.user.team.name,file)

class Task(models.Model):
    title=models.CharField(max_length=100, blank=False, unique=True, verbose_name="Заголовок")
    task=models.TextField(blank=False, verbose_name="Задание")
    task_file=models.FileField(blank=True, null=True, upload_to="tasks/", verbose_name="Файл задания")
    cost=models.PositiveIntegerField(blank=False, null=False, default=0, verbose_name="Максимальный балл за задание")
    deadline=models.DateTimeField(blank=False, null=False, default=datetime.now, verbose_name="Дедлайн")
    created=models.DateTimeField(blank=False, null=False, auto_now_add=True, verbose_name="Создано")
    company=models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Компания")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

class Solution(models.Model):
    team=models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Команда")
    task=models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Задача")
    # solution=models.TextField(blank=False,verbose_name="Решение")
    solution_file=models.FileField(blank=False, null=False, upload_to="solution/", verbose_name="Файл решения")
    score=models.PositiveIntegerField(blank=True, null=True, verbose_name="Баллы за задание")
    created=models.DateTimeField(blank=False, null=False, auto_now_add=True, verbose_name="Создано")
    def __str__(self):
        try:
            return self.task.title
        except:
            return "Не найдено"
    class Meta:
        verbose_name = 'Решение'
        verbose_name_plural = 'Решения'