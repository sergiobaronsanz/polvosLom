# Generated by Django 4.2.7 on 2024-07-20 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0008_granulometria_via_alter_granulometria_d90_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultadostmic',
            name='tiempoEnsayo',
            field=models.CharField(choices=[('1', 'VISUAL'), ('2', 'TERMOPAR'), ('3', 'VISUAL/TERMOPAR')], default='null', max_length=300, verbose_name='Tipo Ensayo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resultadostmic',
            name='tiempoTmax',
            field=models.CharField(choices=[('1', 'VISUAL'), ('2', 'TERMOPAR'), ('3', 'VISUAL/TERMOPAR')], default='null', max_length=300, verbose_name='Tipo Tª max'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ResultadosGranulometria',
        ),
    ]