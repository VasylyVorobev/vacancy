# Generated by Django 3.1.4 on 2021-01-03 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_vacancy_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='published_at',
            field=models.DateField(auto_now_add=True, verbose_name='Опубликовано'),
        ),
    ]
