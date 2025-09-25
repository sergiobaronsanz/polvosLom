from django.db import models
from muestras.models import ListaEnsayos

class Equipos (models.Model):
    tipo_estado = [
        ('0', 'No requiere'),
        ('1', 'Calibrado'),
        ('2', "Calibración caducada"),
        ('3', "Solicitado presupuesto"),
        ('4', "Calibración en curso"),
        ('5', "Esperando certificado"),
        ('6', "Esperando actualización de la ficha del equipo"),
        ('7', 'Verificación al uso')
    ]

    tipo_calibracion = [
        ('0', 'No requiere'),
        ('1', 'Calibración interna'),
        ('2', 'Calibración externa'),
    ]

    tipo_equipo = [
        ('0', 'Controlado'),
        ('1', 'No controlado')
    ]

    codigo= models.CharField(max_length=300, verbose_name="Codigo")
    equipo= models.CharField(max_length=300, verbose_name="Equipo")
    descripcion= models.TextField( verbose_name="Descripcion")
    controlado= models.BooleanField(verbose_name="Controlado")
    ensayos= models.ManyToManyField(ListaEnsayos,verbose_name="Ensayos")
    fechaCalibracion= models.DateField(verbose_name="Fecha de Calibración", null= True, blank=True, default ="2025-09-25")
    fechaCaducidadCalibracion= models.DateField(verbose_name="Fecha próxima calibración", null= True, blank=True, default ="2025-09-25")
    tipoCalibracion = models.CharField(max_length=10, verbose_name= "Tipo Calibración",choices=tipo_calibracion, default='0')
    estadoCalibracion = models.CharField(max_length=10, verbose_name= "Estado Calibración", choices=tipo_estado, default= '0')
    
    class Meta():
        verbose_name="Equipo"
        verbose_name_plural="Equipos"
        
    def __str__(self):
        return f"{self.equipo} | {self.codigo}"
    

class EquipoAsociado(models.Model):
    codigo= models.CharField(max_length=300, verbose_name="Codigo")
    equipo= models.CharField(max_length=300, verbose_name="Equipo")
    equipoAsociado= models.ForeignKey(Equipos, verbose_name="Equipo Asociado", on_delete=models.CASCADE, null=True, blank=True)
    descripcion= models.TextField( verbose_name="Descripcion")
    
    class Meta():
        verbose_name="Equipo asociado"
        verbose_name_plural="Equipos asociados"
        
    def __str__(self):
        return f"{self.codigo} | {self.equipo}"