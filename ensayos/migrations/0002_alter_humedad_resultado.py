# Generated by Django 4.2.7 on 2024-05-05 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='humedad',
            name='resultado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultado_humedad', to='ensayos.resultados', verbose_name='resultado'),
        ),
    ]
