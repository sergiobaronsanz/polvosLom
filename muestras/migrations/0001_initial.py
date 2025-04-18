# Generated by Django 4.2.7 on 2025-04-02 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('expedientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListaEnsayos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ensayo', models.CharField(max_length=300, verbose_name='Ensayo')),
                ('normativa', models.CharField(max_length=300, verbose_name='Normativa')),
                ('poens', models.CharField(max_length=300, verbose_name='POENS')),
            ],
            options={
                'verbose_name': 'Lista Ensayo',
                'verbose_name_plural': 'Listas Ensayos',
            },
        ),
        migrations.CreateModel(
            name='Muestras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_muestra', models.IntegerField(blank=True, null=True, verbose_name='Numero muestra')),
                ('estado', models.CharField(choices=[('1', 'Esperando muestra'), ('2', 'Parada'), ('3', 'Ensayando'), ('4', 'Por revisar'), ('5', 'Terminada')], default='1', max_length=300, verbose_name='Estado')),
                ('observaciones', models.TextField(blank=True, null=True, verbose_name='Observaciones')),
                ('fecha', models.DateField(auto_now_add=True, verbose_name='Fecha')),
                ('fechaComienzo', models.DateField(blank=True, null=True, verbose_name='Fecha comienzo ensayos')),
                ('fechaRevision', models.DateField(blank=True, null=True, verbose_name='Fecha revisión')),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='expedientes.empresa', verbose_name='Empresa')),
                ('expediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expedientes.expedientes', verbose_name='Expediente')),
                ('listaEnsayos', models.ManyToManyField(to='muestras.listaensayos', verbose_name='Ensayos')),
            ],
            options={
                'verbose_name': 'Muestra',
                'verbose_name_plural': 'Muestras',
            },
        ),
        migrations.CreateModel(
            name='DescripcionMuestra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_fabricante', models.CharField(blank=True, max_length=300, null=True, verbose_name='Identificación fabricante')),
                ('fecha_recepcion', models.DateField(blank=True, null=True, verbose_name='Fecha recepción')),
                ('documentacion', models.CharField(blank=True, choices=[('Si', 'Si'), ('No', 'No')], max_length=300, null=True, verbose_name='Documentación')),
                ('etiquetado', models.CharField(choices=[('etiqueta', 'etiqueta'), ('rotulacion', 'rotulacion'), ('sin etiqueta', 'sin etiqueta')], max_length=300, verbose_name='Etiquetado')),
                ('envolturaExt', models.CharField(max_length=300, verbose_name='Envoltura exterior')),
                ('envolturaInt', models.CharField(max_length=300, verbose_name='Envoltura interior')),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Peso')),
                ('procedencia', models.CharField(max_length=300, verbose_name='Procedencia')),
                ('estadoEnvio', models.CharField(max_length=300, verbose_name='Estado del envío')),
                ('aspectoMuestra', models.CharField(max_length=300, verbose_name='Aspecto de la muestra')),
                ('color', models.CharField(max_length=300, verbose_name='Color')),
                ('brillo', models.CharField(max_length=300, verbose_name='Brillo')),
                ('tamano', models.CharField(max_length=300, verbose_name='Tamaño aparente')),
                ('homogeneidad', models.CharField(max_length=300, verbose_name='Homogeneidad')),
                ('formaEnsayo', models.CharField(choices=[('S/V', 'S/V'), ('Preparada', 'Preparada')], max_length=300, verbose_name='¿Como se ensaya?')),
                ('observacion', models.TextField(verbose_name='observaciones')),
                ('imagenMuestra', models.ImageField(blank=True, null=True, upload_to='imagenesMuestras', verbose_name='Imagen muestra')),
                ('imagenEnvoltorio', models.ImageField(blank=True, null=True, upload_to='imagenesMuestras', verbose_name='Imagen envoltorio')),
                ('muestra', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='descripcionmuestra', to='muestras.muestras', verbose_name='Muestra')),
            ],
            options={
                'verbose_name': 'Descripcion muestra',
                'verbose_name_plural': 'Descripciones Muestras',
            },
        ),
    ]
