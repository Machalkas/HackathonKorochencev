# Generated by Django 3.1.2 on 2020-11-26 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0011_auto_20201126_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teams',
            name='id',
        ),
        migrations.AlterField(
            model_name='teams',
            name='name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, unique=True, verbose_name='Название команды'),
        ),
    ]
