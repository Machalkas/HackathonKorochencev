from django.db import models
from django.conf import settings

class Company(models.Model):
    name=models.CharField(max_length=250, blank=False, unique=True, verbose_name="Название")
    description=models.TextField(blank=True, verbose_name="Описание")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

class CompanyRepresentatives(models.Model):
    user_id=models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, verbose_name="Представитель компании")
    company=models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компания")
    class Meta:
        # unique_together = (('user_id', 'company_id'),)
        verbose_name = 'Представитель'
        verbose_name_plural = 'Представители'

