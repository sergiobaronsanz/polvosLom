# Generated by Django 4.2.7 on 2024-08-29 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0030_alter_tmic_resultado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='humedad',
            name='resultado',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='resultadoshumedad',
            name='resultado',
            field=models.CharField(max_length=100, verbose_name='Resultado'),
        ),
    ]
