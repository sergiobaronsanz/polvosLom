# Generated by Django 4.2.7 on 2024-05-26 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0003_remove_kmax_ensayo_remove_kmax_equipos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='humedad',
            name='temperaturaAmbiente',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Temperatura Ambiente'),
        ),
    ]
