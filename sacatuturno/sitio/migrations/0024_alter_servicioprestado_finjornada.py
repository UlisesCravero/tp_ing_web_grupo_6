# Generated by Django 3.2.6 on 2021-10-22 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0023_alter_servicioprestado_finjornada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicioprestado',
            name='finJornada',
            field=models.TimeField(blank=True, default='08:00:00', verbose_name='Fin de Jornada'),
        ),
    ]
