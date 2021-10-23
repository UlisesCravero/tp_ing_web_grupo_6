# Generated by Django 3.2.6 on 2021-10-22 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0018_auto_20211022_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicioprestado',
            name='finJornada',
            field=models.TimeField(blank=True, default='17:00:00', verbose_name='Fin de Jornada'),
        ),
        migrations.AddField(
            model_name='servicioprestado',
            name='inicioJornada',
            field=models.TimeField(blank=True, default='08:00:00', verbose_name='Inicio de Jornada'),
        ),
    ]
