# Generated by Django 4.2.7 on 2025-04-14 07:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('muestras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='descripcionmuestra',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Recepcionado por'),
            preserve_default=False,
        ),
    ]
