# Generated by Django 4.2.7 on 2025-04-07 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0009_remove_pmax_fecha_pmax_fechafin_pmax_fechainicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pmax',
            name='pmax',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, verbose_name='Pmax'),
        ),
        migrations.AlterField(
            model_name='resultadospmax',
            name='pm',
            field=models.DecimalField(decimal_places=1, max_digits=7, verbose_name='PM'),
        ),
    ]
