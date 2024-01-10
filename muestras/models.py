from django.db import models
from expedientes.models import Expedientes, Empresa

# Create your models here.  
class ListaEnsayos(models.Model):
    ensayo= models.CharField(max_length=300, verbose_name="Ensayo")
    normativa= models.CharField(max_length=300, verbose_name="Normativa")
    poens= models.CharField(max_length=300, verbose_name="POENS")
    
    class Meta():
        verbose_name="Lista Ensayo"
        verbose_name_plural="Listas Ensayos"
        
    def __str__(self):
        return f"{self.ensayo}"
    
        
class Muestras(models.Model):
    estados=[
        ("1", "Esperando muestra"),
        ("2", "Parada"),
        ("3", "Ensayando"),
        ("4", "Por revisar"),
        ("5", "Terminada")
    ]
    
    id_muestra=models.IntegerField(verbose_name="Numero muestra", blank= True, null=True)
    expediente= models.ForeignKey(Expedientes, on_delete=models.CASCADE, verbose_name="Expediente")
    empresa= models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Empresa", null=True, blank=True)
    listaEnsayos= models.ManyToManyField(ListaEnsayos, verbose_name="Ensayos")
    estado= models.CharField(choices=estados, max_length=300, verbose_name="Estado", default="1")
    observaciones= models.TextField(verbose_name= "Observaciones", null=True, blank=True)
    fecha= models.DateField(auto_now_add=True, verbose_name="Fecha")
    fechaComienzo= models.DateField(verbose_name="Fecha comienzo ensayos",blank=True, null=True)
    fechaRevision= models.DateField(verbose_name="Fecha revisión", blank=True, null=True)
    
    
    class Meta():
        verbose_name="Muestra"
        verbose_name_plural="Muestras"
        
    def __str__(self):
        return f"{self.empresa} | {self.expediente.empresa.abreviatura}- {self.id_muestra} | {self.expediente}"


class DescripcionMuestra(models.Model):
    etiqueta= [
        ("etiqueta", "etiqueta"),
        ("rotulacion", "rotulacion"),
        ("sin etiqueta", "sin etiqueta"),
    ]
    
    ensayo= [
        ("S/V", "S/V"),
        ("Preparada", "Preparada"),
    ]
    
    documentacion= [
        ("Si", "Si"),
        ("No", "No"),
    ]
    
    
    muestra= models.ForeignKey("Muestras", on_delete=models.CASCADE, related_name= "descripcionmuestra", verbose_name="Muestra", null=True, blank=True)
    id_fabricante= models.CharField(max_length= 300, verbose_name="Identificación fabricante", null=True, blank=True)
    fecha_recepcion= models.DateField(verbose_name="Fecha recepción", null=True, blank=True)
    documentación= models.CharField(max_length= 300, choices=documentacion, verbose_name="Documentación", null=True, blank=True)
    etiquetado= models.CharField(max_length=300, choices=etiqueta, verbose_name="Etiquetado")
    envolturaExt= models.CharField(max_length=300, verbose_name="Envoltura exterior")
    envolturaInt= models.CharField(max_length=300, verbose_name="Envoltura interior")
    peso= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Peso")
    procedencia= models.CharField(max_length=300, verbose_name="Procedencia")
    estadoEnvio=models.CharField(max_length=300, verbose_name="Estado del envío")
    aspectoMuestra=models.CharField(max_length=300, verbose_name="Aspecto de la muestra")
    color=models.CharField(max_length=300, verbose_name="Color")
    brillo=models.CharField(max_length=300, verbose_name="Brillo")
    tamaño=models.CharField(max_length=300, verbose_name="Tamaño aparente")
    homogeneidad= models.CharField(max_length=300, verbose_name="Homogeneidad")
    formaEnsayo=models.CharField(choices=ensayo, max_length=300, verbose_name="¿Como se ensaya?")
    observacion=models.TextField(verbose_name="observaciones")
    imagenMuestra= models.ImageField(verbose_name="Imagen muestra", upload_to="imagenesMuestras", null=True, blank=True)
    imagenEnvoltorio= models.ImageField(verbose_name="Imagen envoltorio",upload_to="imagenesMuestras", null=True, blank=True)
    
    class Meta():
        verbose_name="Descripcion muestra"
        verbose_name_plural="Descripciones Muestras"
        
    def __str__(self):
        return f"{self.peso} | {self.procedencia}"