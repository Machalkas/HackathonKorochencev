# Generated by Django 3.1.2 on 2020-11-04 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0007_auto_20201105_0145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamsleaders',
            name='id',
        ),
        migrations.AlterField(
            model_name='teamsleaders',
            name='team_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, primary_key=True, serialize=False, to='team.teams'),
        ),
    ]
