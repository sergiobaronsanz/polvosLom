# Generated by Django 4.2.7 on 2024-09-07 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0037_remove_resultadosn1_ensayopreseleccion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='n1',
            name='tipoPolvo',
            field=models.CharField(choices=[('1', 'No metalico'), ('2', 'Metalico')], max_length=300, verbose_name='Tipo de polvo'),
        ),
    ]