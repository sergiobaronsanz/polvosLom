# Generated by Django 4.2.7 on 2024-09-22 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0047_alter_n4_fecha_alter_n4_humedad_alter_n4_observacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='o1',
            name='resultado',
            field=models.CharField(blank=True, choices=[('1', 'No se clasifica'), ('2', 'Grupo de embalaje/envasado I/Categoría 1'), ('3', 'Grupo de embalaje/envasado II/Categoría 2'), ('4', 'Grupo de embalaje/envasado III/Categoría 3')], max_length=50, null=True, verbose_name='Resultado'),
        ),
    ]