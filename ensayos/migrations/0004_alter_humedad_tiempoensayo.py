# Generated by Django 4.1 on 2024-01-26 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0003_remove_humedad_manual_remove_humedad_resultado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='humedad',
            name='tiempoEnsayo',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Tiempo de ensayo'),
        ),
    ]
