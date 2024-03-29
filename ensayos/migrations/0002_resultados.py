# Generated by Django 4.2.4 on 2024-01-15 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('muestras', '0013_muestras_estado'),
        ('ensayos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resultados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultado', models.CharField(max_length=100, verbose_name='Resultados')),
                ('unidades', models.CharField(max_length=100, verbose_name='Unidades')),
                ('ensayo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='muestras.listaensayos', verbose_name='Lista ensayos')),
                ('muestra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='muestras.muestras', verbose_name='Muestras')),
            ],
            options={
                'verbose_name': 'Resultado',
                'verbose_name_plural': 'Resultados',
            },
        ),
    ]
