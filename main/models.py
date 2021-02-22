from django.db import models

class Settings(models.Model):
    start_date=models.DateTimeField(blank=True, null=True, verbose_name="Дата начала")
    end_date=models.DateTimeField(blank=True, null=True, verbose_name="Дата окончания")
    max_teams=models.PositiveIntegerField(blank=True, null=True, verbose_name="Максимальное количество команд")
    max_members=models.PositiveIntegerField(blank=True, null=True, verbose_name="Максимальное количество участников в команде")
    class Meta:
        verbose_name = 'Параметры'
        verbose_name_plural = 'Параметры'
    def save(self,*args,**kwargs):
        total_records = Settings.objects.count()
        if total_records >= 1:
            Settings.objects.all().delete()
        super().save(*args,**kwargs)