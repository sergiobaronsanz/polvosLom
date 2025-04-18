# Generated by Django 4.2.7 on 2025-04-02 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('muestras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=300, verbose_name='Codigo')),
                ('equipo', models.CharField(max_length=300, verbose_name='Equipo')),
                ('descripcion', models.TextField(verbose_name='Descripcion')),
                ('controlado', models.BooleanField(verbose_name='Controlado')),
                ('fechaCalibracion', models.DateField(verbose_name='Fecha de Calibración')),
                ('fechaCaducidadCalibracion', models.DateField(verbose_name='Fecha próxima calibración')),
                ('ensayos', models.ManyToManyField(to='muestras.listaensayos', verbose_name='Ensayos')),
                ('equipo_padre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subequipos', to='calidad.equipos', verbose_name='Equipo Padre')),
            ],
            options={
                'verbose_name': 'Equipo',
                'verbose_name_plural': 'Equipos',
            },
        ),
    ]
