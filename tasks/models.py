from django.db import models
from team.models import Teams
from datetime import datetime


class Task(models.Model):
    title=models.CharField(max_length=100, blank=False, unique=True, verbose_name="Заголовок")
    task=models.TextField(blank=False, verbose_name="Задание")
    task_file=models.FileField(blank=True, null=True, verbose_name="Файл задания")
    cost=models.PositiveIntegerField(blank=False, null=False, default=0, verbose_name="Максимальный балл за задание")
    deadline=models.DateTimeField(blank=False, null=False, default=datetime.now, verbose_name="Дедлайн")
    created=models.DateTimeField(blank=False, null=False, auto_now_add=True, verbose_name="Создано")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

class Solution(models.Model):
    team=models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Команда")
    task=models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Задача")
    solution=models.TextField(blank=False,verbose_name="Решение")
    solution_file=models.FileField(blank=True, null=True, verbose_name="Файл решения")
    score=models.PositiveIntegerField(blank=True, null=True, verbose_name="Баллы за задание")
    created=models.DateTimeField(blank=False, null=False, auto_now_add=True, verbose_name="Создано")
    def __str__(self):
        return self.task.title
    class Meta:
        verbose_name = 'Решение'
        verbose_name_plural = 'Решения'