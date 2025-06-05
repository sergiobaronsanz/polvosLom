from django.db import models
from muestras.models import ListaEnsayos

class Equipos (models.Model):
    codigo= models.CharField(max_length=300, verbose_name="Codigo")
    equipo= models.CharField(max_length=300, verbose_name="Equipo")
    descripcion= models.TextField( verbose_name="Descripcion")
    controlado= models.BooleanField(verbose_name="Controlado")
    ensayos= models.ManyToManyField(ListaEnsayos,verbose_name="Ensayos")
    fechaCalibracion= models.DateField(verbose_name="Fecha de Calibración")
    fechaCaducidadCalibracion= models.DateField(verbose_name="Fecha próxima calibración")
    
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
        return f"{self.equipoAsociado} | {self.equipo} | {self.codigo}"