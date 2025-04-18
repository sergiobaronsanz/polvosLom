# Generated by Django 4.2.7 on 2025-04-02 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.CharField(max_length=300, verbose_name='Empresa')),
                ('abreviatura', models.CharField(max_length=100, verbose_name='Abreviatura')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='Expedientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expediente', models.CharField(max_length=100, verbose_name='Nº Expediente')),
                ('estado', models.CharField(choices=[('1', 'Esperando muestra'), ('2', 'Parada'), ('3', 'Ensayando'), ('4', 'Por revisar'), ('5', 'Terminada')], max_length=300, verbose_name='Estado')),
                ('nMuestras', models.IntegerField(blank=True, null=True, verbose_name='Numero de muestras')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expedientes.empresa', verbose_name='Empresa')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
    ]
