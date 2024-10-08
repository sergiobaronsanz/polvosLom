# Generated by Django 4.2.7 on 2024-08-11 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0018_alter_tmic_equipos_alter_tmin_fecha_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lie',
            name='tiempoEnsayo',
        ),
        migrations.AddField(
            model_name='lie',
            name='horasEnsayo',
            field=models.DecimalField(decimal_places=2, default=5, max_digits=5, verbose_name='Tiempo de ensayo'),
        ),
        migrations.AlterField(
            model_name='lie',
            name='boquilla',
            field=models.CharField(blank=True, choices=[('1', 'rebote'), ('2', 'tubular')], max_length=300, null=True, verbose_name='Boquilla'),
        ),
        migrations.AlterField(
            model_name='lie',
            name='cerillas',
            field=models.CharField(blank=True, choices=[('1', 'sobbe'), ('2', 'simex')], max_length=300, null=True, verbose_name='Cerillas'),
        ),
        migrations.AlterField(
            model_name='lie',
            name='fecha',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='lie',
            name='humedad',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Humedad Ambiente'),
        ),
        migrations.AlterField(
            model_name='lie',
            name='resultado',
            field=models.IntegerField(blank=True, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='lie',
            name='temperaturaAmbiente',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Temperatura Ambiente'),
        ),
        migrations.AlterField(
            model_name='lie',
            name='unidad',
            field=models.CharField(blank=True, default='g/m3', max_length=50, null=True, verbose_name='Unidad'),
        ),
    ]
