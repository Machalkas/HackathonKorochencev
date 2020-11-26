from django.db import models
from django.conf import settings

class Teams(models.Model):
    name=models.CharField(max_length=100, primary_key=True, null=False, unique=True, verbose_name="Название команды")
    description=models.TextField(null=True, blank=True, verbose_name="Описание")
    score=models.PositiveSmallIntegerField(default=0, verbose_name="Счет")
    link=models.CharField(max_length=2048 ,null=True, blank=True, verbose_name="Социальные ссылки")
    url=models.CharField(max_length=250, null=True, blank=True, verbose_name="Ссылка для вступления в команду")

    # def __str__(self):
    #     return self.name, self.description, self.link, self.url

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

class TeamsLeaders(models.Model):
    user_id=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team_id=models.OneToOneField(Teams, to_field='name', primary_key=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user_id', 'team_id'),)
