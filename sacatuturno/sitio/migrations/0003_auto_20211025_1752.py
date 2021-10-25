# Generated by Django 3.2.6 on 2021-10-25 20:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitio', '0002_auto_20211025_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='cliente_aux',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha_fin',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 25, 17, 52, 36, 984837), null=True, verbose_name='Fecha Fin'),
        ),
        migrations.AlterField(
            model_name='turno',
            name='fecha_inicio',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 25, 17, 52, 36, 984837), verbose_name='Fecha inicio'),
        ),
    ]
