# Generated by Django 3.1.2 on 2021-01-27 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0007_auto_20210124_2123'),
        ('tasks', '0004_remove_solution_solution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='solution_file',
            field=models.FileField(null=True, upload_to='', verbose_name='Файл решения'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.task', verbose_name='Задача'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='team.teams', verbose_name='Команда'),
        ),
    ]
