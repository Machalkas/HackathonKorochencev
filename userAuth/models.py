from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    specialization = models.CharField(max_length=250, verbose_name="Направление")
    username = None
    email = models.EmailField('Email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

def __str__(self):
    return self.specialization, self.email

# class Meta:
#     verbose_name = 'Профиль'
#     verbose_name_plural = 'Профили'