# Generated by Django 4.2.4 on 2023-12-27 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muestras', '0007_muestras_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='muestras',
            name='observaciones',
            field=models.TextField(blank=True, null=True, verbose_name='Observaciones'),
        ),
    ]