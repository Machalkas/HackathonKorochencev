from django.db import models

class Settings(models.Model):
    start_date=models.DateTimeField(verbose_name="Дата начала")
    max_teams=models.PositiveIntegerField(verbose_name="Максимальное количество команд")
    max_members=models.PositiveIntegerField(verbose_name="Максимальное количество участников в команде")
    class Meta:
        verbose_name = 'Параметры'
        verbose_name_plural = 'Параметры'
    def save(self,*args,**kwargs):
        total_records = Settings.objects.count()
        if total_records >= 1:
            Settings.objects.all().delete()
        super().save(*args,**kwargs)