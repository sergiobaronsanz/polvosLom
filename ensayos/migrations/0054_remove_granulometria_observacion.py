# Generated by Django 4.2.7 on 2025-02-05 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0053_granulometria_observacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='granulometria',
            name='observacion',
        ),
    ]
