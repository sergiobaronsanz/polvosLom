# Generated by Django 4.2.7 on 2025-04-07 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0006_remove_lie_fecha_lie_fechafin_lie_fechainicio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emi',
            name='fecha',
        ),
        migrations.AddField(
            model_name='emi',
            name='fechaFin',
            field=models.DateField(blank=True, null=True, verbose_name='FechaFin'),
        ),
        migrations.AddField(
            model_name='emi',
            name='fechaInicio',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Inicio'),
        ),
    ]
