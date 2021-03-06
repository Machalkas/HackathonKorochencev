# Generated by Django 3.1.2 on 2021-03-07 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210223_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkpoint',
            fields=[
                ('title', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Заголовок')),
                ('start_date', models.DateTimeField(unique=True, verbose_name='Дата начала')),
                ('end_date', models.DateTimeField(unique=True, verbose_name='Дата окончания')),
            ],
            options={
                'verbose_name': 'Чекпоинт',
                'verbose_name_plural': 'Чекпоинты',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('title', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('image', models.ImageField(upload_to='news_image', verbose_name='Изображение')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Имя')),
                ('max', models.PositiveIntegerField(verbose_name='Максимальный балл')),
                ('cof', models.FloatField(verbose_name='Коэффициент')),
            ],
            options={
                'verbose_name': 'Критерий оценки',
                'verbose_name_plural': 'Критерии оценки',
            },
        ),
    ]
