# Generated by Django 4.2.7 on 2024-08-07 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0016_remove_granulometria_tiempoensayo_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tmin',
            old_name='tiempoEnsayo',
            new_name='horasEnsayo',
        ),
        migrations.RemoveField(
            model_name='resultadostmin',
            name='observacion',
        ),
        migrations.AddField(
            model_name='tmin',
            name='observacion',
            field=models.CharField(default='null', max_length=1000, verbose_name='Observacion'),
            preserve_default=False,
        ),
    ]
