from django.db import models

class Settings(models.Model):
    start_date=models.DateTimeField(verbose_name="Дата начала")
    max_teams=models.PositiveIntegerField(verbose_name="Максимальное количество команд")
    max_members=models.PositiveIntegerField(verbose_name="Максимальное количество участников в команде")
    class Meta:
        verbose_name = 'Параметры'
        verbose_name_plural = 'Параметры'