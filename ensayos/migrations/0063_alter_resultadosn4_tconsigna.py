# Generated by Django 4.2.7 on 2025-02-28 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0062_alter_resultadosn4_tmax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultadosn4',
            name='tConsigna',
            field=models.CharField(choices=[('0', 'Selecciona'), ('1', '100'), ('2', '120'), ('3', '140')], max_length=300, verbose_name='Temperatura de la estufa'),
        ),
    ]
