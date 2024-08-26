# Generated by Django 4.2.7 on 2024-08-20 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0022_emi_inductancia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emi',
            name='fecha',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='emi',
            name='fechaAuto',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Fecha automática'),
        ),
        migrations.AlterField(
            model_name='emi',
            name='fechaRev',
            field=models.DateField(auto_now=True, null=True, verbose_name='Fecha revisión'),
        ),
        migrations.AlterField(
            model_name='emi',
            name='humedad',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Humedad Ambiente'),
        ),
        migrations.AlterField(
            model_name='emi',
            name='inductancia',
            field=models.CharField(blank=True, choices=[('1', 'SI'), ('2', 'NO')], max_length=100, null=True, verbose_name='Inductancia'),
        ),
        migrations.AlterField(
            model_name='emi',
            name='observacion',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Observacion'),
        ),
        migrations.AlterField(
            model_name='emi',
            name='presion',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Presión Ambiente'),
        ),
        migrations.AlterField(
            model_name='emi',
            name='resultado',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='emi',
            name='temperaturaAmbiente',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Temperatura Ambiente'),
        ),
        migrations.AlterField(
            model_name='emi',
            name='unidad',
            field=models.CharField(blank=True, default='mJ', max_length=50, null=True, verbose_name='Unidad'),
        ),
    ]
