# Generated by Django 4.2.7 on 2025-06-04 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0031_alter_resultadosclo_dpdt_alter_resultadoslie_dpdt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultadospmax',
            name='peso',
            field=models.IntegerField(verbose_name='Peso equivalente'),
        ),
    ]
