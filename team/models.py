from django.db import models
from django.conf import settings
from tasks.models import Task

class Teams(models.Model):
    name=models.CharField(max_length=100, null=False, unique=True, verbose_name="Название команды")
    description=models.TextField(null=True, blank=True, verbose_name="Описание")
    # score=models.PositiveSmallIntegerField(default=0, verbose_name="Счет")
    link=models.CharField(max_length=255, blank=True, default="", verbose_name="Социальные ссылки")
    url=models.CharField(max_length=255,blank=True, default="", unique=True, verbose_name="Ссылка для вступления в команду")
    task=models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Задание")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

class TeamsLeaders(models.Model):
    user_id=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Лидер")
    team_id=models.OneToOneField(Teams, primary_key=True, on_delete=models.CASCADE, verbose_name="Группа")#to_field='name'
    class Meta:
        unique_together = (('user_id', 'team_id'),)
        verbose_name = 'Лидер'
        verbose_name_plural = 'Лидеры'

class Checked(models.Model):
    checkpoint=models.ForeignKey("main.Checkpoint", on_delete=models.CASCADE, blank=False, null=True, verbose_name="Чекпоинт")
    team=models.ForeignKey(Teams, on_delete=models.CASCADE, blank=False, null=False, verbose_name="Команда")
    score=models.FloatField(blank=True, null=True, default=None, verbose_name="Баллы")
    is_came=models.BooleanField(blank=True, null=True, default=None, verbose_name="Команда пришла")
    def __str__(self):
        return self.checkpoint.title
    class Meta:
        unique_together = (('checkpoint_id', 'team_id'),)
        verbose_name = 'Чекпоинт'
        verbose_name_plural = 'Чекпоинты'
