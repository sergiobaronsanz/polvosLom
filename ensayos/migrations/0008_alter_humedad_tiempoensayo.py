# Generated by Django 4.2.4 on 2024-01-31 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0007_equipos_codigo_equipos_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='humedad',
            name='tiempoEnsayo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Tiempo de ensayo'),
        ),
    ]
