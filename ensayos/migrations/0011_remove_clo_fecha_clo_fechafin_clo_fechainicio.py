# Generated by Django 4.2.7 on 2025-04-07 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0010_alter_pmax_pmax_alter_resultadospmax_pm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clo',
            name='fecha',
        ),
        migrations.AddField(
            model_name='clo',
            name='fechaFin',
            field=models.DateField(blank=True, null=True, verbose_name='FechaFin'),
        ),
        migrations.AddField(
            model_name='clo',
            name='fechaInicio',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Inicio'),
        ),
    ]
