# Generated by Django 4.2.7 on 2024-09-06 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0036_remove_rec_ensayohumedad_n1_resultado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultadosn1',
            name='ensayoPreseleccion',
        ),
        migrations.RemoveField(
            model_name='resultadosn1',
            name='tiempoZonaHumeda',
        ),
        migrations.AddField(
            model_name='n1',
            name='pruebaPreseleccion',
            field=models.CharField(choices=[('1', 'SI'), ('2', 'NO')], default='null', max_length=100, verbose_name='Prueba preselección'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resultadosn1',
            name='zonaHumeda',
            field=models.CharField(blank=True, choices=[('1', 'SI'), ('2', 'NO')], max_length=100, null=True, verbose_name='Tiempo zona húmeda'),
        ),
    ]
