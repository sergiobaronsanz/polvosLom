# Generated by Django 4.2.7 on 2025-02-20 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0058_resultadosemi_numeroensayo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultadosemi',
            name='numeroEnsayo',
            field=models.IntegerField(default=0, verbose_name='Número ensayo'),
        ),
    ]
