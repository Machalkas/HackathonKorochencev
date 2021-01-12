# Generated by Django 3.1.2 on 2021-01-12 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '0004_auto_20210112_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamsleaders',
            name='team_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='team.teams', verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='teamsleaders',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Лидер'),
        ),
    ]
