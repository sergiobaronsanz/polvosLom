# Generated by Django 4.2.7 on 2025-05-23 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muestras', '0002_descripcionmuestra_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='listaensayos',
            name='orden',
            field=models.IntegerField(default=0, verbose_name='Orden'),
            preserve_default=False,
        ),
    ]
