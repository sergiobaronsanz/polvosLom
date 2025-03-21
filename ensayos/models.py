from django.db import models
from muestras.models import Muestras, ListaEnsayos
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404


# Create your models here.

#Resultados
"""class Resultados (models.Model):
    #Hay que cambiar este nombre por lista ensayo y agregar una variable ensayo que seleccione el ensayo en concreto que ha sido, 
    #de esta maner cuando se borre el ensayo se borrarar el resultado
    muestra= models.ForeignKey(Muestras, verbose_name= "Muestras", on_delete= models.CASCADE)
    ensayo= models.ForeignKey(ListaEnsayos, verbose_name= "Lista ensayos", on_delete= models.CASCADE)
    resultado= models.CharField(max_length= 100, verbose_name="Resultado")
    unidades= models.CharField(max_length= 100, verbose_name="Unidades")
    
    class Meta():
        verbose_name="Resultado"
        verbose_name_plural="Resultados"
    
    def __str__(self):
        return f"{self.muestra} | {self.ensayo} -> {self.resultado}
"""
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

#Humedad
class Humedad(models.Model):
    #Obtenemos el valor del ensayo de humedad

    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente", null=True, blank=True)
    humedad=  models.DecimalField(decimal_places=2, max_digits=4, verbose_name="Humedad Ambiente", null=True, blank=True)
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    criterio= models.CharField(default="5", max_length=50, verbose_name="Criterio", null=True, blank=True)
    tDesecacion= models.IntegerField(default=105, verbose_name="Temperatura de Desecación", null=True, blank=True)
    desviacion= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Desviación", null=True, blank=True)
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", null= True, blank= True)
    observacion=models.CharField(max_length=1000, verbose_name="Observación", null=True, blank=True)
    fecha= models.DateField(verbose_name="Fecha", null=True, blank=True)
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True, null=True, blank=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True, null=True, blank=True)
    resultado= models.CharField(verbose_name="Resultado", max_length=100, null=True, blank=True) #99,99%
    unidad= models.CharField(verbose_name="Unidad", max_length=50, default="%", null=True, blank=True)

    horasEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=1)
    
    def save(self, *args, **kwargs):
        # Obtener el objeto ListaEnsayos para "Humedad"
        humedad = get_object_or_404(ListaEnsayos, ensayo="Humedad")
        self.ensayo = humedad
        super(Humedad, self).save(*args, **kwargs)


    class Meta():
        verbose_name="Humedad"
        verbose_name_plural="Humedades"
        
    def __str__(self):
        return f"{self.muestra}"

class ResultadosHumedad(models.Model):
    ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    resultado= models.CharField(max_length=100, verbose_name="Resultado")

    
    class Meta():
        verbose_name="Resultado Humedad"
        verbose_name_plural="Resultados Humedades"
        
    def __str__(self):
        return f"{self.ensayo} | {self.resultado}"

#Granulometría
class Granulometria(models.Model):
    vias=[
        ("1", "Seca"),
        ("2", "Húmeda"),
    ]

    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente",null= True, blank= True)
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente",null= True, blank= True)
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    
    fecha= models.DateField(verbose_name="Fecha",null= True, blank= True)
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True,null= True, blank= True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True,null= True, blank= True)
    via= models.CharField(choices=vias, verbose_name="Vía", null= True, blank= True, max_length=100)
    d10= models.DecimalField(verbose_name="d10", max_digits=7, decimal_places=3,null= True, blank= True)#9999.999
    d50= models.DecimalField(verbose_name="d50", max_digits=7, decimal_places=3,null= True, blank= True)#9999.999
    d90= models.DecimalField(verbose_name="d90", max_digits=7, decimal_places=3,null= True, blank= True)#9999.999
    resultado= models.DecimalField(verbose_name="d50", max_digits=7, decimal_places=3,null= True, blank= True)#9999.999 es diempre la d50
    unidad= models.CharField(verbose_name="Unidad", max_length=50, default= "um",null= True, blank= True)

    archivo= models.FileField(upload_to="archivosGranulometria")
    horasEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=1)

    
    class Meta():
        verbose_name="Humedad"
        verbose_name_plural="Humedades"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

    

#TMIc
class TMIc (models.Model):
    funde_muestra=[
        ("1", "SI"),
        ("2", "NO")
    ]

    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente", blank=True, null=True)
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente", blank=True, null=True)
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    tiempoMaxEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo máximo del ensayo", blank=True, null=True)
    fecha= models.DateField(verbose_name="Fecha", blank=True, null=True)
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True, blank=True, null=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True, blank=True, null=True)
    resultado= models.CharField(verbose_name="Resultado", max_length=100, blank=True, null=True) #399,99
    funde= models.CharField(choices= funde_muestra,verbose_name="Funde", max_length=50, default="2", blank=True, null=True)
    unidad= models.CharField(verbose_name="Unidad", max_length=50, default="ºC", blank=True, null=True)
    observacion=models.CharField(max_length=1000, verbose_name="Observacion", default="null", blank=True, null=True)

    horasEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=5)

    class Meta():
        verbose_name="TMIc"
        verbose_name_plural="TMIcs"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

class ResultadosTMIc (models.Model):
    resultadosPosibles=[
        ("1", "SI"),
        ("2", "NO"),
        ("3", "FUNDE"),
        ("4", "NO FUNDE"),
    ]
    
    ignicionesPosibles=[
        ("1", "VISUAL"),
        ("2", "TERMOPAR"),
        ("3", "VISUAL/TERMOPAR")
    ]
    
    ensayo= models.ForeignKey("TMIc", on_delete=models.CASCADE, verbose_name="Ensayo TMIc")
    tPlato= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura plato",null= True, blank= True)
    tMaxima= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura máxima", null= True, blank= True)
    resultado= models.CharField(max_length=300, choices=resultadosPosibles, verbose_name= "resultado", null= True, blank= True)
    tipoIgnicion= models.CharField(max_length=300, choices=ignicionesPosibles, verbose_name="Tipo ignición", null= True, blank= True)
    tiempoPrueba= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo ensayo", null= True, blank= True)
    tiempoTmax= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo a temperatura máxima", null= True, blank= True)

    
    class Meta():
        verbose_name="Resultado TMIc"
        verbose_name_plural="Resultados TMIc"
        
    def __str__(self):
        return f"{self.ensayo.muestra} | {self.tPlato} | {self.get_resultado_display()}"
    

#TMIn
class TMIn (models.Model):
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente", blank=True, null=True)
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente", blank=True, null=True)
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    fecha= models.DateField(verbose_name="Fecha", blank=True, null=True)
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True, blank=True, null=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True, blank=True, null=True)
    resultado= models.CharField(verbose_name="Resultado",max_length=100, blank=True, null=True) #999,99
    unidad= models.CharField(verbose_name="Unidad", max_length=50, default="ºC", blank=True, null=True)
    observacion=models.CharField(max_length=1000, verbose_name="Observacion", blank=True, null=True)
    
    horasEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=1)
    
    class Meta():
        verbose_name="TMIn"
        verbose_name_plural="TMIns"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

class ResultadosTMIn (models.Model):
    resultadosPosibles=[
        ("1", "SI"),
        ("2", "NO"),
    ]
    
    ensayo= models.ForeignKey("TMIn", on_delete=models.CASCADE, verbose_name="Ensayo TMIn")
    tHorno= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura horno")
    peso= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Peso")
    presion= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Presión")
    resultado= models.CharField(max_length=300, choices=resultadosPosibles, verbose_name= "resultado")
    
    class Meta():
        verbose_name="Resultado TMIn"
        verbose_name_plural="Resultados TMIn"
        
    def __str__(self):
        return f"{self.ensayo} | {self.resultado}"
    

#LIE
class LIE (models.Model):
    seleccionCerillas = [
        ("1", "sobbe"),
        ("2", "simex"),
    ]

    
    seleccionBoquillas = [
        ("1", "rebote"),
        ("2", "tubular"),
    ]

    
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente", null=True, blank=True)
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente", null=True, blank=True)
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    cerillas= models.CharField(max_length=300, choices=seleccionCerillas, verbose_name="Cerillas", null=True, blank=True)
    boquilla= models.CharField(max_length=300, choices=seleccionBoquillas, verbose_name="Boquilla", null=True, blank=True)
    fecha= models.DateField(verbose_name="Fecha", null=True, blank=True)
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    resultado= models.CharField(verbose_name="Resultado", max_length=100, null=True, blank=True) #125, 250
    unidad= models.CharField(verbose_name="Unidad", max_length=50, default="g/m3", null=True, blank=True)
    observacion=models.CharField(max_length=1000, verbose_name="Observacion")

    horasEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=5)

    class Meta():
        verbose_name="LIE"
        verbose_name_plural="LIE"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

class ResultadosLIE (models.Model):
    resultadosPosibles = [
        ("1", "SI"),
        ("2", "NO"),
    ]
    
    ensayo= models.ForeignKey("LIE", on_delete=models.CASCADE, verbose_name="Ensayo LIE")
    concentracion= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Concentración")
    peso= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Peso equivalente")
    pex= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="PEX")
    pm= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="PM")
    dpdt= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="dP/dT")
    resultado= models.CharField(max_length=300, choices=resultadosPosibles, verbose_name= "resultado")
    
    
    class Meta():
        verbose_name="Resultado LIE"
        verbose_name_plural="Resultados LIE"
        
    def __str__(self):
        return f"{self.ensayo} | {self.resultado}"
    

#Emi
class EMI (models.Model):
    selecionInductancia= [
        ("1", "SI"),
        ("2", "NO")
    ]

    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente", blank= True, null= True)
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente", blank= True, null= True)
    presion= models.DecimalField(decimal_places=2, max_digits=7, verbose_name="Presión Ambiente", blank= True, null= True)
    inductancia= models.CharField(max_length=100, choices=selecionInductancia, verbose_name="Inductancia", blank= True, null= True)
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    fecha= models.DateField(verbose_name="Fecha", blank= True, null= True)
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True, blank= True, null= True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True, blank= True, null= True)
    resultado= models.CharField(verbose_name="Resultado", max_length=100, blank= True, null= True) #9999,99
    unidad= models.CharField(verbose_name="Unidad", max_length=50, default="mJ", blank= True, null= True)
    observacion=models.CharField(max_length=1000, verbose_name="Observacion", blank= True, null= True)

    horasEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=1)

    class Meta():
        verbose_name="Emi"
        verbose_name_plural="Emis"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

class ResultadosEMI (models.Model):
    resultadosPosibles = [
        ("1", "SI"),
        ("2", "NO"),
    ]

    
    ensayo= models.ForeignKey("EMI", on_delete=models.CASCADE, verbose_name="Ensayo Emi")
    concentracion= models.IntegerField(verbose_name="Concentracion")
    energia= models.IntegerField(verbose_name="Energia")
    retardo= models.IntegerField(verbose_name="Retardo")
    resultado= models.CharField(max_length=300, choices=resultadosPosibles, verbose_name= "resultado")
    numeroEnsayo= models.IntegerField(verbose_name="Número ensayo", default=0)
    
    
    class Meta():
        verbose_name="Resultado Emi"
        verbose_name_plural="Resultados Emi"
        
    def __str__(self):
        return f"{self.ensayo} | {self.resultado}"
    

#Pmax
class Pmax (models.Model):
    seleccionCerillas = [
        ("1", "simex"),
        ("2", "sobbe"),
    ]

    
    seleccionBoquillas = [
        ("1", "rebote"),
        ("2", "tubular"),
    ]
    
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente", blank= True, null= True)
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente", blank= True, null= True)
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    cerillas= models.CharField(max_length=300, choices=seleccionCerillas, verbose_name="Cerillas", blank= True, null= True)
    boquilla= models.CharField(max_length=300, choices=seleccionBoquillas, verbose_name="Boquilla", blank= True, null= True)
    fecha= models.DateField(verbose_name="Fecha", blank= True, null= True)
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    pmax= models.DecimalField(verbose_name="Pmax", max_digits=4, decimal_places=2, blank= True, null= True) #99,99
    dpdt= models.IntegerField(verbose_name="dPdT", blank= True, null= True) #999
    kmax= models.IntegerField(verbose_name="kmax", blank= True, null= True)
    unidadPmax= models.CharField(verbose_name="Unidad", max_length=50, default="bar", blank= True, null= True)
    unidadDpdt= models.CharField(verbose_name="Unidad", max_length=50, default="bar/s", blank= True, null= True)
    observacion=models.CharField(max_length=1000, verbose_name="Observacion", blank= True, null= True)

    horasEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=5)

    class Meta():
        verbose_name="Pmax"
        verbose_name_plural="Pmaxs"
        
    def __str__(self):
        return f"{self.muestra} | Pmax: {self.pmax}, dP/dT: {self.dpdt}, kmax: {self.kmax}" 

class ResultadosPmax (models.Model):
    seriesPosibles = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
    ]

    
    ensayo= models.ForeignKey("Pmax", on_delete=models.CASCADE, verbose_name="Ensayo Pmax")
    concentracion= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Concentración")
    peso= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Peso equivalente")
    serie= models.CharField(max_length=300, choices=seriesPosibles, verbose_name= "Serie")
    pm= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="PM")
    dpdt= models.IntegerField( verbose_name="dP/dT")
    
    class Meta():
        verbose_name="Resultado Pmax"
        verbose_name_plural="Resultados Pmaxs"
        
    def __str__(self):
        return f"{self.ensayo} | Pmax: {self.pm}, dP/dT: {self.dpdt} "



#clo
class CLO (models.Model):
    seleccionCerillas = [
        ("1", "simex"),
        ("2", "sobbe"),
    ]

    
    seleccionBoquillas = [
        ("1", "rebote"),
        ("2", "tubular"),
    ]
    
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente", null= True, blank= True)
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente", null= True, blank= True)
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    cerillas= models.CharField(max_length=300, choices=seleccionCerillas, verbose_name="Cerillas", null= True, blank= True)
    boquilla= models.CharField(max_length=300, choices=seleccionBoquillas, verbose_name="Boquilla", null= True, blank= True)
    fecha= models.DateField(verbose_name="Fecha", null= True, blank= True)
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    resultado= models.CharField(verbose_name="Resultado", max_length=100, null= True, blank= True) #9999,99
    unidad= models.CharField(verbose_name="Unidad", max_length=50, default="%", null= True, blank= True)
    observacion=models.CharField(max_length=1000, verbose_name="Observacion", null= True, blank= True)

    horasEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=5)

    class Meta():
        verbose_name="LIE"
        verbose_name_plural="LIE"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

class ResultadosCLO (models.Model):
    resultadosPosibles = [
        ("1", "SI"),
        ("2", "NO"),
    ]

    
    ensayo= models.ForeignKey("CLO", on_delete=models.CASCADE, verbose_name="Ensayo LIE")
    concentracion= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Concentración")
    peso= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Peso equivalente")
    pex= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="PEX")
    pm= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="PM")
    dpdt= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="dP/dT")
    oxigeno= models.IntegerField(verbose_name= "Oxígeno")
    resultado= models.CharField(max_length=300, choices=resultadosPosibles, verbose_name= "resultado")
    
    class Meta():
        verbose_name="Resultado CLO"
        verbose_name_plural="Resultados CLO"
        
    def __str__(self):
        return f"{self.ensayo} | {self.resultado}"
    

#N1
class N1 (models.Model):
    polvos = [
        ("1", "No metalico"),
        ("2", "Metalico"),
        
    ]

    
    resultadosPosibles = [
        ("1", "No se clasifica"),
        ("2", "Grupo de embalaje/envasado II/ Categoría 1"),
        ("3", "Grupo de embalaje/envasado III/ Categoría 2")
    ]

    preseleccion= [
        ("1", "SI"),
        ("2", "NO")
    ]
    
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente", null= True, blank= True)
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente", null= True, blank= True)
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    tipoPolvo=models.CharField(max_length=300, choices= polvos, verbose_name="Tipo de polvo", null= True, blank= True)
    pruebaPreseleccion= models.CharField(choices= preseleccion, verbose_name="Prueba preselección", max_length=100, null= True, blank= True)
    resultado= models.CharField(choices=resultadosPosibles, verbose_name="Resultado", max_length=100, null= True, blank= True)
    fecha= models.DateField(verbose_name="Fecha", null= True, blank= True)
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    observacion=models.CharField(max_length=1000, verbose_name="Observacion", null= True, blank= True)

    horasEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=5)
    """resultado= models.DecimalField(verbose_name="Resultado", max_digits=6, decimal_places=2, null=True) #9999,99
    unidad= models.CharField(verbose_name="Unidad", max_length=50, default="mJ")"""
    
    class Meta():
        verbose_name="N1"
        verbose_name_plural="N1s"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

class ResultadosN1 (models.Model):
    rebasa= [
        ("1", "SI"),
        ("2", "NO")
    ]

    ensayo= models.ForeignKey("N1", on_delete=models.CASCADE, verbose_name="Ensayo TMIn")
    tiempo= models.IntegerField(verbose_name="Tiempo")
    zonaHumeda= models.CharField(choices=rebasa, max_length=100, verbose_name="Tiempo zona húmeda", blank=True, null=True)
    
    class Meta():
        verbose_name="Resultado N1"
        verbose_name_plural="Resultados N1"
        
    def __str__(self):
        return f"{self.ensayo} | Tiempo: {self.tiempo}"
    

#N2
class N2 (models.Model):
    resultadosPosibles = [
        ("1", "No se clasifica"),
        ("2", "Grupo de embalaje/ envasado I / Categoría 1")
    ]

    
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente", blank= True, null= True)
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente", blank= True, null= True)
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    fecha= models.DateField(verbose_name="Fecha", blank= True, null= True)
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    resultado= models.CharField(choices=resultadosPosibles, verbose_name="resultado", max_length=100, blank= True, null= True)
    observacion=models.CharField(max_length=1000, verbose_name="Observacion", blank= True, null= True)

    horasEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=1)
    """resultado= models.DecimalField(verbose_name="Resultado", max_digits=6, decimal_places=2, null=True) #9999,99
    unidad= models.CharField(verbose_name="Unidad", max_length=50, default="mJ")"""
    
    class Meta():
        verbose_name="N2"
        verbose_name_plural="N2s"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

class ResultadosN2 (models.Model):
    resultadosPosibles = [
        ("1", "SI"),
        ("2", "NO"),
    ]

    ensayo= models.ForeignKey("N2", on_delete=models.CASCADE, verbose_name="Ensayo N2")
    resultado= models.CharField(max_length=300, choices=resultadosPosibles, verbose_name= "Resultado")
    
    class Meta():
        verbose_name="Resultado N2"
        verbose_name_plural="Resultados N2"
        
    def __str__(self):
        return f"{self.ensayo} | {self.resultado}"
    
    
#N4
class N4 (models.Model):   
    resultadosPosibles = [
        ("1", "No se clasifica"),
        ("2", "Grupo embalaje/envasado II/Categoría 1 "),
        ("3", "Exenta si se transporta en bultos <3 m3"),
        ("4", "Grupo embalaje/envasado III/Categoría 2"),
        ("5", "Exenta si se transporta en bultos <450 litros")
    ]

    
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente", blank= True, null= True)
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente", blank= True, null= True)
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    fecha= models.DateField(verbose_name="Fecha", blank= True, null= True)
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    resultado= models.CharField(choices=resultadosPosibles, verbose_name="resultado", max_length=100, blank= True, null= True)

    observacion=models.CharField(max_length=1000, verbose_name="Observacion", blank= True, null= True)

    horasEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=4)
    """resultado= models.DecimalField(verbose_name="Resultado", max_digits=6, decimal_places=2, null=True) #9999,99
    unidad= models.CharField(verbose_name="Unidad", max_length=50, default="mJ")"""
    
    class Meta():
        verbose_name="N4"
        verbose_name_plural="N4"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

class ResultadosN4 (models.Model):
    resultadosPosibles = [
        ("1", "SI"),
        ("2", "NO"),
    ]

    celdasDisponibles=[
        ("1", "25 mm"),
        ("2", "100 mm"),
    ]

    temperaturasDisponibles=[
        ("0", "Selecciona"),
        ("1", "100"),
        ("2", "120"),
        ("3", "140"),
    ]
    
    ensayo= models.ForeignKey("N4", on_delete=models.CASCADE, verbose_name="Ensayo N4")
    celda= models.CharField(max_length=300, choices=celdasDisponibles, verbose_name="Celdas")
    tConsigna= models.CharField(max_length=300,verbose_name="Temperatura de la estufa", choices=temperaturasDisponibles )
    tMax= models.DecimalField(decimal_places=2, max_digits=6, verbose_name="Temperatura máxima")
    tiempo= models.IntegerField(verbose_name="Tiempo")
    resultado= models.CharField(max_length=300, choices=resultadosPosibles, verbose_name= "resultado")
    
    class Meta():
        verbose_name="Resultado N4"
        verbose_name_plural="Resultados N4"
        
    def __str__(self):
        return f"{self.ensayo} | Celda: {self.celda},Temperatura estufa: {self.tconsigna}, Tiempo: {self.tiempo}, Temperatura máxima: {self.tMax}" 
   
#En revisión
"""#N5
class N5 (models.Model):   
    resultadosPosibles={
        ["1", "No se clasifica"],
        ["2", "Grupo embalaje/envasado I/Categoría 1"],
        ["3", "Grupo embalaje/envasado II/Categoría 2"],
        ["4", "Grupo embalaje/envasado III/Categoría 3"],
    }
    
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente")
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente")
    presion= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Presión Ambiente")
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    celda100= models.BooleanField(verbose_name="Celda 100 mm")
    celda25= models.BooleanField(verbose_name="Celda 25 mm")
    resultado= models.CharField(choices=resultadosPosibles, verbose_name="Resultado")
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=1)
    fecha= models.DateField(verbose_name="Fecha")
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    
    class Meta():
        verbose_name="N4"
        verbose_name_plural="N4"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

class ResultadosN4 (models.Model):
    resultadosPosibles={
        ["SI", "SI"],
        ["NO", "NO"],
    }
    celdasDisponibles={
        ["1", "25 mm"],
        ["2", "1000 mm"],
    }
    
    ensayo= models.ForeignKey("N4", on_delete=models.CASCADE, verbose_name="Ensayo N4")
    celda= models.CharField(choices=celdasDisponibles, verbose_name="Celdas")
    tconsigna= models.IntegerField(verbose_name="Temperatura de la estufa")
    tMax= models.DecimalField(decimal_places=5, max_digits=4, verbose_name="Temperatura máxima")
    tiempo= models.IntegerField(verbose_name="Tiempo")
    resultado= models.CharField(max_length=300, choices=resultadosPosibles, verbose_name= "resultado")
    observacion=models.CharField(max_length=1000, verbose_name="Observacion")
    
    class Meta():
        verbose_name="Resultado N4"
        verbose_name_plural="Resultados N4"
        
    def __str__(self):
        return f"{self.ensayo} | Celda: {self.celda},Temperatura estufa: {self.tconsigna}, Tiempo: {self.tiempo}, Temperatura máxima: {self.tMax}" 
   
"""

#O1
class O1 (models.Model): 
    
    resultadosPosibles = [
        ("1", "No se clasifica"),
        ("2", "Grupo de embalaje/envasado I/Categoría 1"),
        ("3", "Grupo de embalaje/envasado II/Categoría 2"),
        ("4", "Grupo de embalaje/envasado III/Categoría 3")
    ]
    
    
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente", blank=True, null= True)
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente", blank=True, null= True)
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    ensayoHumedad= models.FileField(upload_to='ensayos/o1/humedad_celulosa/', verbose_name="Humedad Celulosa", blank=True, null= True)
    fecha= models.DateField(verbose_name="Fecha", blank=True, null= True)
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True, blank=True, null= True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True, blank=True, null= True)
    resultado= models.CharField(max_length=50, choices= resultadosPosibles, verbose_name="Resultado", blank=True, null=True) #9999,99
    observacion=models.CharField(max_length=1000, verbose_name="Observacion", blank=True, null= True)

    horasEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=5)
    
    #unidad= models.CharField(verbose_name="Unidad", max_length=50, default="mJ")"""
    
    
    class Meta():
        verbose_name="O1"
        verbose_name_plural="O1"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

class ResultadosO1 (models.Model):
    
    porcentajes = [
        ("1", "30/70"),
        ("2", "60/40"),
        ("3", "40/60"),
        ("4", "50/50"),
        ("2", "80/20")
    ]


    ensayo= models.ForeignKey("O1", on_delete=models.CASCADE, verbose_name="Ensayo O1")
    ensayoReferencia= models.BooleanField(verbose_name="¿Ensayo Referencia?")
    proporcion= models.CharField(max_length=300,choices= porcentajes, verbose_name="Proporción")
    tiempo1= models.IntegerField(verbose_name="Tiempo1")
    tiempo2= models.IntegerField(verbose_name="Tiempo2")
    tiempo3= models.IntegerField(verbose_name="Tiempo3")
    tiempo4= models.IntegerField(verbose_name="Tiempo4")
    tiempo5= models.IntegerField(verbose_name="Tiempo5")
    resultado= models.IntegerField(verbose_name= "Resultado", blank=True, null= True)
    
    class Meta():
        verbose_name="Resultado O1"
        verbose_name_plural="Resultados O1"
        
    def __str__(self):
        return f"{self.ensayo} | Proporciones: {self.proporcion},Tiempo: {self.tiempo}" 
   

#REC
class REC (models.Model):  
    
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente", null= True, blank= True)
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente", null= True, blank= True)
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    fecha= models.DateField(verbose_name="Fecha", null= True, blank= True)
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    resultado= models.DecimalField(verbose_name="Resultado", max_digits=12, decimal_places=2, null= True, blank= True) #9999,99
    unidad= models.CharField(verbose_name="Unidad", max_length=50, default="Mohm", null= True, blank= True)
    observacion=models.CharField(max_length=1000, verbose_name="Observacion", null= True, blank= True)

    horasEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=5)
    
    class Meta():
        verbose_name="REC"
        verbose_name_plural="REC"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

class ResultadosREC (models.Model):
    
    tensiones = [
        ("1", "100"),
        ("2", "500"),
        ("3", "1000")
    ]


    ensayo= models.ForeignKey("REC", on_delete=models.CASCADE, verbose_name="Ensayo REC")
    tension= models.IntegerField(verbose_name= "Resultado", blank=True, null= True)
    tiempo= models.IntegerField(verbose_name="Tiempo")
    resultado= models.DecimalField(decimal_places=2, max_digits=8, verbose_name= "Resultado", blank=True, null= True)
    
    class Meta():
        verbose_name="Resultado REC"
        verbose_name_plural="Resultados REC"
        
    def __str__(self):
        return f"{self.ensayo} | Proporciones: {self.Tension},Tiempo: {self.tiempo}, Resultado: {self.resultado}" 
   

#TRATAMIENTO
class Tratamiento (models.Model): 
    
    preseleccion= [
        ("1", "NO"),
        ("2", "SI")    
    ]
    
    tamices= [
        ("1", "500"),
        ("2", "1000"),
        ("2", "250"),
        ("2", "800"),
        ("2", "125"),
        ("2", "63"),
    ]
    
    
    
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE,  verbose_name="Ensayo")
    
    secado= models.CharField(verbose_name="Secado", choices=preseleccion, max_length=500, default=None, blank= True, null= True)
    equipoSecado= models.ManyToManyField("Equipos",  verbose_name="Equipos de secado", related_name="tratamientos_equipoSecado",default=None)
    fechaSecadoInicio= models.DateField(verbose_name="Fecha", blank=True, null= True)
    fechaSecadoFin= models.DateField(verbose_name="Fecha", blank=True, null= True)
    temperatura= models.IntegerField(verbose_name="Temperatura", blank= True, null= True)
    tiempo= models.IntegerField(verbose_name="Tiempo", blank= True, null= True)

    molido= models.CharField(verbose_name="Molido", choices=preseleccion, max_length=500, default=None, blank= True, null= True)
    equipoMolido= models.ManyToManyField("Equipos",  verbose_name="Equipos de molienda",related_name="tratamientos_equipoMolido",default=None)
    fechaMolidoInicio= models.DateField(verbose_name="Fecha", blank=True, null= True)
    fechaMolidoFin= models.DateField(verbose_name="Fecha", blank=True, null= True)

    tamizado= models.CharField(verbose_name="Tamizado", choices=preseleccion, max_length=500, default=None, blank= True, null= True)
    equipoTamizado= models.ManyToManyField("Equipos",  verbose_name="Equipos de tamizado",related_name="tratamientos_equipoTamizado",default=None)
    fechaTamizadoInicio= models.DateField(verbose_name="Fecha", blank=True, null= True)
    fechaTamizadoFin= models.DateField(verbose_name="Fecha", blank=True, null= True)

    horasEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=5)
    
    
    class Meta():
        verbose_name="Tratamiento"
        verbose_name_plural="Tratamientos"
        
    def __str__(self):
        return f"{self.muestra} tratada" 
