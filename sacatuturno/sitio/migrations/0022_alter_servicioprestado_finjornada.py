# Generated by Django 3.2.6 on 2021-10-22 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0021_alter_servicioprestado_finjornada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicioprestado',
            name='finJornada',
            field=models.TimeField(blank=True, verbose_name='Fin de Jornada'),
        ),
    ]
