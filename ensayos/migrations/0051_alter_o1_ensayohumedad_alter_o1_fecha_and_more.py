# Generated by Django 4.2.7 on 2024-10-26 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0050_resultadoso1_tiempo1_resultadoso1_tiempo2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='o1',
            name='ensayoHumedad',
            field=models.FileField(blank=True, null=True, upload_to='ensayos/o1/humedad_celulosa/', verbose_name='Humedad Celulosa'),
        ),
        migrations.AlterField(
            model_name='o1',
            name='fecha',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='o1',
            name='fechaAuto',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Fecha automática'),
        ),
        migrations.AlterField(
            model_name='o1',
            name='fechaRev',
            field=models.DateField(auto_now=True, null=True, verbose_name='Fecha revisión'),
        ),
        migrations.AlterField(
            model_name='o1',
            name='humedad',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Humedad Ambiente'),
        ),
        migrations.AlterField(
            model_name='o1',
            name='observacion',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Observacion'),
        ),
        migrations.AlterField(
            model_name='o1',
            name='temperaturaAmbiente',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Temperatura Ambiente'),
        ),
    ]