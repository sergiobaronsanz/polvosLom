# Generated by Django 4.2.7 on 2024-09-07 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0038_alter_n1_tipopolvo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='n1',
            name='fecha',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='n1',
            name='humedad',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Humedad Ambiente'),
        ),
        migrations.AlterField(
            model_name='n1',
            name='observacion',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Observacion'),
        ),
        migrations.AlterField(
            model_name='n1',
            name='pruebaPreseleccion',
            field=models.CharField(blank=True, choices=[('1', 'SI'), ('2', 'NO')], max_length=100, null=True, verbose_name='Prueba preselección'),
        ),
        migrations.AlterField(
            model_name='n1',
            name='resultado',
            field=models.CharField(blank=True, choices=[('1', 'No se clasifica'), ('2', 'Grupo de embalaje/envasado II/ Categoría 1'), ('3', 'Grupo de embalaje/envasado III/ Categoría 2')], max_length=100, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='n1',
            name='temperaturaAmbiente',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Temperatura Ambiente'),
        ),
        migrations.AlterField(
            model_name='n1',
            name='tipoPolvo',
            field=models.CharField(blank=True, choices=[('1', 'No metalico'), ('2', 'Metalico')], max_length=300, null=True, verbose_name='Tipo de polvo'),
        ),
        migrations.AlterField(
            model_name='rec',
            name='fecha',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='rec',
            name='humedad',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Humedad Ambiente'),
        ),
        migrations.AlterField(
            model_name='rec',
            name='observacion',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Observacion'),
        ),
        migrations.AlterField(
            model_name='rec',
            name='resultado',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Resultado'),
        ),
        migrations.AlterField(
            model_name='rec',
            name='temperaturaAmbiente',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Temperatura Ambiente'),
        ),
        migrations.AlterField(
            model_name='rec',
            name='unidad',
            field=models.CharField(blank=True, default='Mohm', max_length=50, null=True, verbose_name='Unidad'),
        ),
    ]
