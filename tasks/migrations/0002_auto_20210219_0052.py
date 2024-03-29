# Generated by Django 3.1.2 on 2021-02-18 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '0001_initial'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='team.teams', verbose_name='Команда'),
        ),
        migrations.AlterUniqueTogether(
            name='solution',
            unique_together={('team', 'task')},
        ),
    ]
