# Generated by Django 4.2.4 on 2023-12-28 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muestras', '0010_descripcionmuestra_id_fabricante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descripcionmuestra',
            name='id_fabricante',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Identificación fabricante'),
        ),
    ]
