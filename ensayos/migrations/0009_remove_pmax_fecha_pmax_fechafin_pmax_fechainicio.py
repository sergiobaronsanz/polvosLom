# Generated by Django 4.2.7 on 2025-04-07 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0008_remove_emisin_fecha_emisin_fechafin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pmax',
            name='fecha',
        ),
        migrations.AddField(
            model_name='pmax',
            name='fechaFin',
            field=models.DateField(blank=True, null=True, verbose_name='FechaFin'),
        ),
        migrations.AddField(
            model_name='pmax',
            name='fechaInicio',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Inicio'),
        ),
    ]
