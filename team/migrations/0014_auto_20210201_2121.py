# Generated by Django 3.1.2 on 2021-02-01 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0013_auto_20210201_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teams',
            name='name',
            field=models.CharField(max_length=10, verbose_name='Название команды'),
        ),
        migrations.AlterField(
            model_name='teams',
            name='url',
            field=models.CharField(blank=True, default='', max_length=10, verbose_name='Ссылка для вступления в команду'),
        ),
    ]