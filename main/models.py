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

class News(models.Model):
    title=models.CharField(max_length=255, primary_key=True, null=False, blank=False, verbose_name="Заголовок")
    text=models.TextField(null=False, blank=False, verbose_name="Текст")
    image=models.ImageField(upload_to="news_image", verbose_name="Изображение")
    created=models.DateTimeField(blank=False, null=False, auto_now_add=True, verbose_name="Создано")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Rating(models.Model):
    name=models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name="Имя")
    max=models.PositiveIntegerField(null=False, blank=False, verbose_name="Максимальный балл")
    cof=models.FloatField(null=False, blank=False, verbose_name='Коэффициент')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Критерий оценки'
        verbose_name_plural = 'Критерии оценки'

class Checkpoint(models.Model):
    title=models.CharField(max_length=100, unique=True, blank=False, null=False, verbose_name="Заголовок")
    start_date=models.DateTimeField(null=False, blank=False, unique=True, verbose_name="Дата начала")
    end_date=models.DateTimeField(null=False, blank=False, unique=True, verbose_name="Дата окончания")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Чекпоинт'
        verbose_name_plural = 'Чекпоинты'