from django.db import models
from django.core.exceptions import ValidationError

#для сжатия
from io import BytesIO
from PIL import Image
from django.core.files import File
def compress(image):
    im = Image.open(image)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=60) 
    new_image = File(im_io, name=image.name)
    return new_image

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
    def clean(self):
        if self.start_date!=None and self.end_date!=None:
            c=Checkpoint.objects.all()
            for i in c:
                if i.start_date<self.start_date or i.start_date>self.end_date:
                    raise ValidationError({"start_date":'Чекпоинт "'+i.title+'" не попадает в указанный диапазон дат'})
                if i.end_date<self.start_date or i.end_date>self.end_date:
                    raise ValidationError({"end_date":'Чекпоинт "'+i.title+'" не попадает в указанный диапазон дат'})


class News(models.Model):
    title=models.CharField(max_length=255, null=False, blank=False, verbose_name="Заголовок")
    text=models.TextField(null=False, blank=False, verbose_name="Текст")
    image=models.ImageField(upload_to="news_image", verbose_name="Изображение")
    created=models.DateTimeField(blank=False, null=False, auto_now_add=True, verbose_name="Создано")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
    def save(self, *args, **kwargs):
        new_image = compress(self.image)
        self.image = new_image
        super().save(*args, **kwargs)


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
    class Meta:
        verbose_name = 'Чекпоинт'
        verbose_name_plural = 'Чекпоинты'
    def __str__(self):
        return self.title
    def clean(self):
        if self.start_date!=None and self.end_date!=None:
            s=Settings.objects.all()
            c=Checkpoint.objects.all()
            if self.start_date>=self.end_date:
                raise ValidationError("Дата начала должна быть меньше даты конца")
            if len(s)>0 and (self.start_date<s[0].start_date or self.start_date>s[0].end_date or self.end_date<s[0].start_date or self.end_date>s[0].end_date):
                raise ValidationError("Даты начала и конца должны находится в промежутке между "+ str(s[0].start_date)+" и "+str(s[0].end_date))
            for i in c:
                if(self.id!=i.id):
                    if (self.start_date<=i.end_date and self.start_date>=i.start_date) or (self.end_date<=i.end_date and self.end_date>=i.start_date):
                        raise ValidationError('Введенные даты пересикаются с чекпоинтом "'+i.title+'"')
                    if (self.start_date>i.start_date and self.end_date<i.end_date) or (self.start_date<i.start_date and self.end_date>i.end_date):
                        raise ValidationError('Включает или включен в чекпоинт "'+i.title+'"')