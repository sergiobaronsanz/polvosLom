# Generated by Django 4.2.7 on 2025-04-04 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0004_remove_tmic_fecha_tmic_fechafin_tmic_fechainicio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tmin',
            name='fecha',
        ),
        migrations.AddField(
            model_name='tmin',
            name='fechaFin',
            field=models.DateField(blank=True, null=True, verbose_name='FechaFin'),
        ),
        migrations.AddField(
            model_name='tmin',
            name='fechaInicio',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Inicio'),
        ),
    ]
