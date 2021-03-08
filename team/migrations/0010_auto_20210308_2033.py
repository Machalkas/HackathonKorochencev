# Generated by Django 3.1.2 on 2021-03-08 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_checkpoint'),
        ('team', '0009_auto_20210308_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checked',
            name='checkpoint',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.checkpoint', verbose_name='Чекпоинт'),
        ),
        migrations.AlterUniqueTogether(
            name='checked',
            unique_together={('checkpoint_id', 'team_id')},
        ),
    ]
