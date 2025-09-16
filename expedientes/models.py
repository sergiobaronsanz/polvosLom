from django.db import models



# Create your models here.
class Empresa(models.Model):
    empresa= models.CharField(max_length=300, verbose_name="Empresa")
    abreviatura= models.CharField(max_length=100, verbose_name="Abreviatura")
    
    class Meta():
        verbose_name="Empresa"
        verbose_name_plural="Empresas"
    def __str__(self):
        return f"{self.empresa}"
    
    
class Expedientes(models.Model):
    estados=[
        ("1", "Esperando muestra"),
        ("2", "Parada"),
        ("3", "Ensayando"),
        ("4", "Por revisar"),
        ("5", "Terminada")
    ]
    
    expediente= models.CharField(max_length=100, verbose_name="Nº Expediente")
    empresa= models.ForeignKey("Empresa", on_delete=models.CASCADE, verbose_name="Empresa")
    empresaContrata= models.CharField(verbose_name="Empresa subcontrata", max_length=300, default="", blank= True, null=True)
    estado=models.CharField(choices=estados, max_length=300, verbose_name="Estado")
    nMuestras=models.IntegerField(verbose_name="Numero de muestras", blank=True, null=True)
    fecha= models.DateField(auto_now_add=True)
    porcentaje= models.DecimalField(decimal_places=2, max_digits= 5, verbose_name="Porcentaje ensayado", default=0)
    
    class Meta():
        verbose_name="Empresa"
        verbose_name_plural="Empresas"
        
    def __str__(self):
        return f"{self.expediente}"
    
    
