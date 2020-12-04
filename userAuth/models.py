from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.models import PermissionsMixin
from team.models import Teams

class Manager(UserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Пользователь должен иметь email')
        user=self.model(email=email,)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, first_name, last_name, password=None):
        user=self.model(email=email,first_name=first_name,last_name=last_name)
        # user.username=""
        user.is_staff=True
        user.is_superuser=True
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    specialization = models.CharField(max_length=250, verbose_name="Направление")
    username = None
    email = models.EmailField('Email', unique=True)
    team=models.ForeignKey(Teams, models.SET_NULL, null=True, blank=True, verbose_name="Команда")
    is_specialist=models.BooleanField(default=False, verbose_name="Специалист")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects=Manager()

    # def __str__(self):
    #     return self.team.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
