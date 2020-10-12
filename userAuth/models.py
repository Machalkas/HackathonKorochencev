from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.models import PermissionsMixin

class Manager(UserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Пользователь должен иметь email')
        user=self.model(email=email,)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None):
        user=self.model(email=email,)
        user.username=""
        user.is_staff=True
        user.is_superuser=True
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    specialization = models.CharField(max_length=250, verbose_name="Направление")
    username = None
    email = models.EmailField('Email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects=Manager()

def __str__(self):
    return self.specialization, self.email

class Meta:
    verbose_name = 'Профиль'
    verbose_name_plural = 'Профили'

