# Generated by Django 3.1.2 on 2021-02-19 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='specialization',
            field=models.CharField(blank=True, max_length=250, verbose_name='Направление'),
        ),
    ]
