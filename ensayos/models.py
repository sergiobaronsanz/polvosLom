from django.db import models
from muestras.models import Muestras, ListaEnsayos

# Create your models here.

#Resultados
class Resultados (models.Model):
    muestra= models.ForeignKey(Muestras, verbose_name= "Muestras", on_delete= models.CASCADE)
    ensayo= models.ForeignKey(ListaEnsayos, verbose_name= "Lista ensayos", on_delete= models.CASCADE)
    resultado= models.CharField(max_length= 100, verbose_name="Resultados")
    unidades= models.CharField(max_length= 100, verbose_name="Unidades")
    
    class Meta():
        verbose_name="Resultado"
        verbose_name_plural="Resultados"
    
    def __str__(self):
        return f"{self.muestra} | {self.ensayo} -> {self.resultado}"
    
class Equipos (models.Model):
    equipo= models.CharField(max_length=300, verbose_name="Equipo")
    controlado= models.BooleanField(verbose_name="Controlado")
    fechaCalibracion= models.DateField(verbose_name="Fecha de Calibración")
    fechaCaducidadCalibracion= models.DateField(verbose_name="Fecha próxima calibración")
    
    class Meta():
        verbose_name="Equipo"
        verbose_name_plural="Equipos"
        
    def __str__(self):
        return f"{self.equipo} | {self.controlado}"

#Humedad
class Humedad(models.Model):
    muestra= models.ForeignKey( Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente")
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente")
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    criterio= models.IntegerField(default=5, verbose_name="Criterio")
    manual=models.BooleanField(verbose_name="Manual")
    tDesecacion= models.IntegerField(default=105, verbose_name="Temperatura de Desecación")
    desviacion= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Desviación")
    resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=1)
    fecha= models.DateField(verbose_name="Fecha")
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    
    class Meta():
        verbose_name="Humedad"
        verbose_name_plural="Humedades"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}"

class ResultadosHumedad(models.Model):
    ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    observacion=models.CharField(max_length=1000, verbose_name="Observación")
    
    class Meta():
        verbose_name="Resultado Humedad"
        verbose_name_plural="Resultados Humedades"
        
    def __str__(self):
        return f"{self.ensayo} | {self.resultado}"

#Granulometría
class Granulometria(models.Model):
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente")
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente")
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=1)
    fecha= models.DateField(verbose_name="Fecha")
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    
    class Meta():
        verbose_name="Humedad"
        verbose_name_plural="Humedades"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

class ResultadosGranulometria(models.Model):
    ensayo= models.ForeignKey("Granulometria", on_delete=models.CASCADE, verbose_name="Ensayo Granulometría")
    d10= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="d10")
    d50= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="d50")
    d90= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="d90")
    observacion=models.CharField(max_length=1000, verbose_name="Observacion")
    
    class Meta():
        verbose_name="Resultado Granulometria"
        verbose_name_plural="Resultados Granulometria"
        
    def __str__(self):
        return f"{self.ensayo} | {self.resultado}"
    

#TMIc
class TMIc (models.Model):
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente")
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente")
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=5)
    fecha= models.DateField(verbose_name="Fecha")
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    
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
        ("4 FUNDE", "NO FUNDE"),
    ]
    
    ignicionesPosibles=[
        ("1", "VISUAL"),
        ("2", "TERMOPAR"),
        ("3", "VISUAL/TERMOPAR")
    ]
    
    ensayo= models.ForeignKey("TMIc", on_delete=models.CASCADE, verbose_name="Ensayo TMIc")
    tPlato= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura plato")
    tMaxima= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura máxima")
    resultado= models.CharField(max_length=300, choices=resultadosPosibles, verbose_name= "resultado")
    tipoIgnicion= models.CharField(max_length=300, choices=ignicionesPosibles, verbose_name="Tipo ignición")
    observacion=models.CharField(max_length=1000, verbose_name="Observacion")
    
    class Meta():
        verbose_name="Resultado TMIc"
        verbose_name_plural="Resultados TMIc"
        
    def __str__(self):
        return f"{self.ensayo} | {self.resultado}"
    

#TMIn
class TMIn (models.Model):
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente")
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente")
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=1)
    fecha= models.DateField(verbose_name="Fecha")
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    
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
    observacion=models.CharField(max_length=1000, verbose_name="Observacion")
    
    class Meta():
        verbose_name="Resultado TMIn"
        verbose_name_plural="Resultados TMIn"
        
    def __str__(self):
        return f"{self.ensayo} | {self.resultado}"
    

#LIE
class LIE (models.Model):
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
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente")
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente")
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    cerillas= models.CharField(max_length=300, choices=seleccionCerillas, verbose_name="Cerillas")
    boquilla= models.CharField(max_length=300, choices=seleccionBoquillas, verbose_name="Boquilla")
    resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=2)
    fecha= models.DateField(verbose_name="Fecha")
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    
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
    observacion=models.CharField(max_length=1000, verbose_name="Observacion")
    
    class Meta():
        verbose_name="Resultado LIE"
        verbose_name_plural="Resultados LIE"
        
    def __str__(self):
        return f"{self.ensayo} | {self.resultado}"
    

#Emi
class EMI (models.Model):
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente")
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente")
    presion= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Presión Ambiente")
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=1)
    fecha= models.DateField(verbose_name="Fecha")
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    
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
    concentracion= models.DecimalField(decimal_places=4, max_digits=5, verbose_name="Concentracion")
    energia= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Energia")
    retardo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Retardo")
    resultado= models.CharField(max_length=300, choices=resultadosPosibles, verbose_name= "resultado")
    observacion=models.CharField(max_length=1000, verbose_name="Observacion")
    
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
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente")
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente")
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    cerillas= models.CharField(max_length=300, choices=seleccionCerillas, verbose_name="Cerillas")
    boquilla= models.CharField(max_length=300, choices=seleccionBoquillas, verbose_name="Boquilla")
    resultadoPmax= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado Pmax")
    resultadoDpdt= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado dpDt")   
    resultadoKmax= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado kMax") 
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=5)
    fecha= models.DateField(verbose_name="Fecha")
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    
    class Meta():
        verbose_name="Pmax"
        verbose_name_plural="Pmaxs"
        
    def __str__(self):
        return f"{self.muestra} | Pmax: {self.resultadoPmax}, dP/dT: {self.resultadoDpdt}, kmax: {self.resultadoKmax}" 

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
    pex= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="PEX")
    pm= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="PM")
    dpdt= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="dP/dT")
    observacion=models.CharField(max_length=1000, verbose_name="Observacion")
    
    class Meta():
        verbose_name="Resultado Pmax"
        verbose_name_plural="Resultados Pmaxs"
        
    def __str__(self):
        return f"{self.ensayo} | Pmax: {self.pm}, Pex: {self.pex}, dP/dT: {self.dpdt} "
    

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
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente")
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente")
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    cerillas= models.CharField(max_length=300, choices=seleccionCerillas, verbose_name="Cerillas")
    boquilla= models.CharField(max_length=300, choices=seleccionBoquillas, verbose_name="Boquilla")
    resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=5)
    fecha= models.DateField(verbose_name="Fecha")
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    
    class Meta():
        verbose_name="LIE"
        verbose_name_plural="LIE"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

class ResultadosClo (models.Model):
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
    resultado= models.CharField(max_length=300, choices=resultadosPosibles, verbose_name= "resultado")
    observacion=models.CharField(max_length=1000, verbose_name="Observacion")
    
    class Meta():
        verbose_name="Resultado CLO"
        verbose_name_plural="Resultados CLO"
        
    def __str__(self):
        return f"{self.ensayo} | {self.resultado}"
    

#N1
class N1 (models.Model):
    polvos = [
        ("1", "Metalico"),
        ("2", "No metalico")
    ]

    
    resultadosPosibles = [
        ("1", "No se clasifica"),
        ("2", "Grupo de embalaje/envasado II/ Categoría 1"),
        ("3", "Grupo de embalaje/envasado III/ Categoría 2")
    ]

    
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente")
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente")
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    tipoPolvo=models.CharField(max_length=300, choices= polvos, verbose_name="Tipo de polvo")
    resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=3)
    fecha= models.DateField(verbose_name="Fecha")
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    
    class Meta():
        verbose_name="N1"
        verbose_name_plural="N1s"
        
    def __str__(self):
        return f"{self.muestra} | {self.resultado}" 

class ResultadosN1 (models.Model):
       
    ensayo= models.ForeignKey("TMIn", on_delete=models.CASCADE, verbose_name="Ensayo TMIn")
    ensayoPreseleccion= models.BooleanField(verbose_name="¿Ensayo de preselección?")
    tiempo= models.IntegerField(verbose_name="Tiempo")
    tiempoZonaHumeda= models.IntegerField(verbose_name="Tiempo zona húmeda", blank=True, null=True)
    observacion=models.CharField(max_length=1000, verbose_name="Observacion")
    
    class Meta():
        verbose_name="Resultado N1"
        verbose_name_plural="Resultados N1"
        
    def __str__(self):
        return f"{self.ensayo} | Tiempo: {self.tiempo}, TIempo zona Húmeda: {self.tiempoZonaHumeda}"
    

#N2
class N2 (models.Model):
    resultadosPosibles = [
        ("1", "No se clasifica"),
        ("2", "Grupo de embalaje/ envasado I / Categoría 1")
    ]

    
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente")
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente")
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    resultado= models.CharField(max_length= 500,choices=resultadosPosibles, verbose_name="Resultado")
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=1)
    fecha= models.DateField(verbose_name="Fecha")
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    
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
    observacion=models.CharField(max_length=1000, verbose_name="Observacion")
    
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
        ("4", "Grupo embalaje/envasado III/Categoría 2")
    ]

    
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente")
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente")
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    celda100= models.BooleanField(verbose_name="Celda 100 mm")
    celda25= models.BooleanField(verbose_name="Celda 25 mm")
    resultado= models.CharField(max_length= 500, choices=resultadosPosibles, verbose_name="Resultado")
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=4)
    fecha= models.DateField(verbose_name="Fecha")
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    
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
        ("2", "1000 mm"),
    ]
    
    ensayo= models.ForeignKey("N4", on_delete=models.CASCADE, verbose_name="Ensayo N4")
    celda= models.CharField(max_length=300, choices=celdasDisponibles, verbose_name="Celdas")
    tconsigna= models.IntegerField(verbose_name="Temperatura de la estufa")
    tMax= models.DecimalField(decimal_places=4, max_digits=5, verbose_name="Temperatura máxima")
    tiempo= models.IntegerField(verbose_name="Tiempo")
    resultado= models.CharField(max_length=300, choices=resultadosPosibles, verbose_name= "resultado")
    observacion=models.CharField(max_length=1000, verbose_name="Observacion")
    
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
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente")
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente")
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    resultado= models.CharField(max_length= 500, choices=resultadosPosibles, verbose_name="Resultado")
    ensayoHumedad= models.FileField(upload_to='ensayos/o1/humedad_celulosa/', verbose_name="Humedad Celulosa")
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=5)
    fecha= models.DateField(verbose_name="Fecha")
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    
    
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
    tiempo= models.IntegerField(verbose_name="Tiempo")
    resultado= models.IntegerField(verbose_name= "Resultado", blank=True, null= True)
    observacion=models.CharField(max_length=1000, verbose_name="Observacion")
    
    class Meta():
        verbose_name="Resultado O1"
        verbose_name_plural="Resultados O1"
        
    def __str__(self):
        return f"{self.ensayo} | Proporciones: {self.proporcion},Tiempo: {self.tiempo}" 
   

#REC
class REC (models.Model):  
    
    muestra= models.ForeignKey(Muestras, on_delete=models.CASCADE, verbose_name="Muestra")
    ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo")
    temperaturaAmbiente= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Temperatura Ambiente")
    humedad=  models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Humedad Ambiente")
    equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    ensayoHumedad= models.FileField(upload_to='ensayos/o1/humedad_celulosa/', verbose_name="Humedad Celulosa")
    tiempoEnsayo= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Tiempo de ensayo", default=1)
    fecha= models.DateField(verbose_name="Fecha")
    fechaAuto= models.DateField(verbose_name="Fecha automática", auto_now_add=True)
    fechaRev= models.DateField(verbose_name="Fecha revisión", auto_now=True)
    
    
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
    tension= models.DecimalField(decimal_places=2, max_digits=5, verbose_name= "Resultado", blank=True, null= True)
    tiempo= models.IntegerField(verbose_name="Tiempo")
    resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name= "Resultado", blank=True, null= True)
    observacion=models.CharField(max_length=1000, verbose_name="Observacion")
    
    class Meta():
        verbose_name="Resultado REC"
        verbose_name_plural="Resultados REC"
        
    def __str__(self):
        return f"{self.ensayo} | Proporciones: {self.Tension},Tiempo: {self.tiempo}, Resultado: {self.resultado}" 
   

