# Generated by Django 4.2.7 on 2025-02-28 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0061_alter_resultadosrec_tension'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultadosn4',
            name='tMax',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Temperatura máxima'),
        ),
    ]
