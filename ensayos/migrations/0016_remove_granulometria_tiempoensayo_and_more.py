# Generated by Django 4.2.7 on 2024-08-06 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0015_alter_tmic_equipos_alter_tmic_fecha_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='granulometria',
            name='tiempoEnsayo',
        ),
        migrations.RemoveField(
            model_name='tmic',
            name='tiempoEnsayo',
        ),
        migrations.AddField(
            model_name='granulometria',
            name='horasEnsayo',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5, verbose_name='Tiempo de ensayo'),
        ),
        migrations.AddField(
            model_name='humedad',
            name='horasEnsayo',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5, verbose_name='Tiempo de ensayo'),
        ),
        migrations.AddField(
            model_name='tmic',
            name='horasEnsayo',
            field=models.DecimalField(decimal_places=2, default=5, max_digits=5, verbose_name='Tiempo de ensayo'),
        ),
    ]
