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
    
    equipo_padre = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="subequipos", 
        verbose_name="Equipo Padre"
    )
    
    class Meta():
        verbose_name="Equipo"
        verbose_name_plural="Equipos"
        
    def __str__(self):
        if self.equipo_padre:
            return f"{self.equipo_padre} | {self.codigo} | {self.equipo}"
        else:
            return f"{self.equipo} | {self.codigo}"