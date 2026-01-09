from django import forms
from ensayos.models import Humedad, Granulometria 
from muestras.models import ListaEnsayos
from muestras.models import Muestras
from calidad.models import Equipos, EquipoAsociado
from django.db.models import Q
from django.shortcuts import  get_object_or_404, get_list_or_404
from django.forms import formset_factory




#HUMEDAD
class HumedadForm(forms.Form):
    #Todos los campos # se deben establecer en la view
    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #desviacion= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Desviación")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo", default=ensayo_humedad)
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")"""

    muestras= Muestras.objects.all()

    criterios= [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('manual', 'Manual'),
    ]

    
    muestra = forms.ModelChoiceField(
        queryset=muestras,
        label="Muestra",
        empty_label="Selecciona una muestra",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    fechaInicio= forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )
    
    fechaFin= forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )


    temperaturaAmbiente = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )

    humedad= forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Humedad Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )

    criterio= forms.ChoiceField(
        choices=criterios,
        label="Criterio",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        initial= "5"
    )

    #Solo si el criterio es manual
    tiempoEnsayo= forms.DecimalField(
        decimal_places=2,  
        label="Tiempo de ensayo", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    tDesecacion= forms.IntegerField(
        initial=105, 
        label="Temperatura de Desecación",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )
    
    desviacion= forms.DecimalField(
        decimal_places=2,  
        label="Desviacion", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly': 'readonly', 'style': 'text-align: center;'}),
    )
    

    resultado1= forms.CharField(
        label="Resultado-1", 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado2= forms.CharField(  
        label="Resultado-2", 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado3= forms.CharField( 
        label="Resultado-3", 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado4= forms.CharField( 
        label="Resultado-4", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado5= forms.CharField(
        label="Resultado-5", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado6= forms.CharField(
        label="Resultado-6", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado7= forms.CharField(
        label="Resultado-7", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado8= forms.CharField(  
        label="Resultado-8", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado9= forms.CharField(  
        label="Resultado-9", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado10= forms.CharField( 
        label="Resultado-10", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )


    observacion=forms.CharField(
        label= "Observación",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

#GRANULO
class GranulometriaForm(forms.Form):
    #Todos los campos # se deben establecer en la view
    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")"""

    vias=[
        ("1", "Seca"),
        ("2", "Húmeda"),
    ]

    muestras= Muestras.objects.all()

    
    muestra = forms.ModelChoiceField(
        queryset=muestras,
        label="Muestra",
        empty_label="Selecciona una muestra",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    fechaInicio= forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaFin= forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )


    temperaturaAmbiente = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )

    humedad= forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Humedad Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )

    via= forms.ChoiceField(
        choices= vias,
        label= "Vía",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    d10= forms.DecimalField(
        decimal_places=3,  
        label="d10", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    d50= forms.DecimalField(
        decimal_places=3,  
        label="d50", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    d90= forms.DecimalField(
        decimal_places=3,  
        label="d90", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    archivo= forms.FileField(
        label= "Archivo",
        required= True,

    )



    observacion=forms.CharField(
        label= "Observación",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

#TMIC
class TmicForm(forms.Form):
    #Todos los campos # se deben establecer en la view
    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    #tiempoEnsayo 

    funde_muestra=[
        ("1", "SI"),
        ("2", "NO")
    ]
    
    muestras= Muestras.objects.all()

    
    muestra = forms.ModelChoiceField(
        queryset=muestras,
        label="Muestra",
        empty_label="Selecciona una muestra",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    fechaInicio= forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaFin= forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )


    temperaturaAmbiente = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )

    humedad= forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Humedad Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )
    
    presion= forms.DecimalField(
        decimal_places=2,
        max_digits=6,
        label="Presión",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    ) 

    tiempoMaxEnsayo=forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label= "Tiempo máximo del ensayo",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )
    

    observacion=forms.CharField(
        label= "Observación",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

class TmicResultadosForm(forms.Form):
    resultadosPosibles=[
        ('', 'Selecciona'),
        ("1", "SI"),
        ("2", "NO"),
        ("3", "FUNDE"),
        ("4", "NO FUNDE"),
    ]
    
    ignicionesPosibles=[
        ('', 'Selecciona'),
        ("1", "VISUAL"),
        ("2", "TERMOPAR"),
        ("3", "VISUAL/TERMOPAR")
    ]

    tPlato= forms.IntegerField(
        label="Temperatura Plato (ºC)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'required': 'required'}),
        required=False,
    )

    tMax= forms.DecimalField(
        decimal_places=2,  
        label="Temperatura máxima (ªC)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    resultadoPrueba= forms.ChoiceField(
        choices=resultadosPosibles,
        label= "Resultado",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,

    )

    tipoIgnicion= forms.ChoiceField(
        choices=ignicionesPosibles,
        label= "Tipo ignición",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    tiempoPrueba= forms.IntegerField(
        label= "Tiempo total (min)",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'required':'required'}),
        required=False,

    )

    tiempoMax= forms.IntegerField(
        label= "Tiempo Tmax (min)",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )
    
tmicResultadosFormSet= formset_factory(TmicResultadosForm, extra=7)

#TMIn
class TminForm(forms.Form):
    #Todos los campos # se deben establecer en la view
    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    #tiempoEnsayo 
    
    muestras= Muestras.objects.all()

    
    muestra = forms.ModelChoiceField(
        queryset=muestras,
        label="Muestra",
        empty_label="Selecciona una muestra",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    fechaInicio= forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaFin= forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )


    temperaturaAmbiente = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )

    humedad= forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Humedad Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )  
    
    presion= forms.DecimalField(
        decimal_places=2,
        max_digits=6,
        label="Presión",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    ) 

    observacion=forms.CharField(
        label= "Observación",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

class TminResultadosForm(forms.Form):
    resultadosPosibles=[
        ('', 'Selecciona'),
        ("1", "SI"),
        ("2", "NO"),
    ]

    tHorno= forms.IntegerField( 
        label="Temperatura Horno (ºC)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'required': 'required'}),
        required=False,
    )

    peso= forms.DecimalField(
        decimal_places=2,  
        label="Peso (g)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'required': 'required',}),
        required=False,
    )

    presion= forms.IntegerField( 
        label= "Presion (kPa)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'required': 'required'}),
        required=False,
    )

    resultadoPrueba= forms.ChoiceField(
        choices=resultadosPosibles,
        label= "Resultado",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,

    )
    
    repeticiones= forms.IntegerField(
        label= "Repeticiones",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )
    

tminResultadosFormSet= formset_factory(TminResultadosForm, extra=7)

#LIE
class LieForm(forms.Form):
    #Todos los campos # se deben establecer en la view
    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    #tiempoEnsayo 

    seleccionCerillas = [
        ("1", "sobbe"),
        ("2", "simex"),
    ]

    
    seleccionBoquillas = [
        ("1", "rebote"),
        ("2", "tubular"),
    ]


    muestras= Muestras.objects.all()

    
    muestra = forms.ModelChoiceField(
        queryset=muestras,
        label="Muestra",
        empty_label="Selecciona una muestra",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    fechaInicio= forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaFin= forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )


    temperaturaAmbiente = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )

    temperaturaEsfera = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Esfera",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )

    humedad= forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Humedad Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )  

    cerillas= forms.ChoiceField(
            choices= seleccionCerillas,
            label= "Cerillas",
            widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
            required=False,

    )

    boquilla= forms.ChoiceField(
            choices= seleccionBoquillas,
            label= "Boquilla",
            widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
            required=False,

    )

    observacion=forms.CharField(
        label= "Observación",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

class LieResultadosForm(forms.Form):
    resultadosPosibles=[
        ('', 'Selecciona'),
        ("1", "SI"),
        ("2", "NO"),
    ]

    concentracion= forms.DecimalField(
        decimal_places=2,  
        label="Concentración (g/m3)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'required': 'true', 'style': 'text-align: center;'}),
        required=False,
    )

    peso= forms.DecimalField(
        decimal_places=1,  
        label="Peso (g)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly': 'readonly', 'required': 'true', 'style': 'text-align: center;'}),
        required=False,
    )

    pex= forms.DecimalField(
        decimal_places=1,  
        label= "Pex (bar)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'required': 'true', 'style': 'text-align: center;'}),
        required=False,
    )

    pm= forms.DecimalField(
        decimal_places=1,  
        label= "Pm (bar)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'required': 'true', 'style': 'text-align: center;'}),
        required=False,
    )

    dpdt= forms.IntegerField( 
        label= "dP/dT (bar/s)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'required': 'true', 'style': 'text-align: center;'}),
        required=False,
    )

    resultadoPrueba= forms.ChoiceField(
        choices=resultadosPosibles,
        label= "Resultado",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'required': 'true', 'style': 'text-align: center;'}),
        required=False,

    )
    

lieResultadosFormSet= formset_factory(LieResultadosForm, extra=7)

#EMI

class EmiForm(forms.Form):
    #Todos los campos # se deben establecer en la view
    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    #tiempoEnsayo 

    selecionInductancia= [
        ("1", "SI"),
        ("2", "NO")
    ]


    muestras= Muestras.objects.all()

    
    muestra = forms.ModelChoiceField(
        queryset=muestras,
        label="Muestra",
        empty_label="Selecciona una muestra",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    fechaInicio= forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaFin= forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )


    temperaturaAmbiente = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )
    

    humedad= forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Humedad Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )  

    presion= forms.DecimalField(
        decimal_places=2,
        max_digits=6,
        label="Presión",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    ) 


    inductancia= forms.ChoiceField( 
        choices= selecionInductancia,
        label= "Inductancia",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm','style': 'text-align: center;'}),
        required=True,
    )

    resultado= forms.DecimalField(
        decimal_places=1,
        max_digits=6,
        label="Resultado (Es)",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    observacion=forms.CharField(
        label= "Observación",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

class EmiResultadosForm(forms.Form):
    resultadosPosibles=[
        ('', 'Selecciona'),
        ("1", "SI"),
        ("2", "NO"),
    ]

    concentracion= forms.IntegerField(
        label="Concentración (g/m3)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    energia= forms.IntegerField(
        label="Energía (mJ)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    retardo= forms.IntegerField(
        label= "Retardo (ms)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )


    resultadoPrueba= forms.ChoiceField(
        choices=resultadosPosibles,
        label= "Resultado",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm resultadosPruebas', 'style': 'text-align: center;'}),
        required=False,
    )

    numeroEnsayo = forms.IntegerField(
        label="Nº Ensayo",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
        min_value=1,
        max_value=10,
    )

    

emiResultadosFormSet= formset_factory(EmiResultadosForm, extra=7)

#PMAX
class PmaxForm(forms.Form):
    #Todos los campos # se deben establecer en la view
    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    #tiempoEnsayo 

    seleccionCerillas = [
        ("1", "sobbe"),
        ("2", "simex"),
    ]

    
    seleccionBoquillas = [
        ("1", "rebote"),
        ("2", "tubular"),
    ]


    muestras= Muestras.objects.all()

    
    muestra = forms.ModelChoiceField(
        queryset=muestras,
        label="Muestra",
        empty_label="Selecciona una muestra",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    
    fechaInicio= forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaFin= forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )


    temperaturaAmbiente = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )

    temperaturaEsfera = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Esfera",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )

    humedad= forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Humedad Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )  

    cerillas= forms.ChoiceField(
            choices= seleccionCerillas,
            label= "Cerillas",
            widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
            required=False,

    )

    boquilla= forms.ChoiceField(
            choices= seleccionBoquillas,
            label= "Boquilla",
            widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
            required=False,

    )

    pm_media= forms.DecimalField(
        decimal_places=1,
        max_digits=5,
        label="Presión media",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly': 'readonly','style': 'text-align: center;'})
    )

    dpdt_media= forms.IntegerField(
        label="dP/dT media",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly': 'readonly','style': 'text-align: center;'})
    )

    kmax= forms.IntegerField(
        label="kmax",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly': 'readonly','style': 'text-align: center;'})
    )

    observacion=forms.CharField(
        label= "Observación",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

class PmaxResultadosForm(forms.Form):

    seriesPosibles = [
        ("", "Selecciona"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
    ]

    concentracion= forms.IntegerField(
        label="Concentración (g/m3)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    peso= forms.DecimalField(  
        decimal_places=1,
        label="Peso (g)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly': 'readonly', 'style': 'text-align: center;'}),
        required=False,
    )

    serie= forms.ChoiceField(
        choices=seriesPosibles,
        label= "Series",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )


    pm_serie= forms.DecimalField(
        decimal_places=1,  
        label= "Pm (bar)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    dpdt_serie= forms.IntegerField(  
        label= "dP/dT (bar/s)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )


pmaxResultadosFormSet= formset_factory(PmaxResultadosForm, extra=7)

#CLO
class CloForm(forms.Form):
    #Todos los campos # se deben establecer en la view
    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    #tiempoEnsayo 

    seleccionCerillas = [
        ("1", "sobbe"),
        ("2", "simex"),
    ]

    
    seleccionBoquillas = [
        ("1", "rebote"),
        ("2", "tubular"),
    ]


    muestras= Muestras.objects.all()

    
    muestra = forms.ModelChoiceField(
        queryset=muestras,
        label="Muestra",
        empty_label="Selecciona una muestra",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    fechaInicio= forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm',  'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaFin= forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )


    temperaturaAmbiente = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )

    temperaturaEsfera = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Esfera",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )

    humedad= forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Humedad Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )  

    cerillas= forms.ChoiceField(
            choices= seleccionCerillas,
            label= "Cerillas",
            widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
            required=False,

    )

    boquilla= forms.ChoiceField(
            choices= seleccionBoquillas,
            label= "Boquilla",
            widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
            required=False,

    )

    observacion=forms.CharField(
        label= "Observación",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

class CloResultadosForm(forms.Form):
    resultadosPosibles=[
        ('', 'Selecciona'),
        ("1", "SI"),
        ("2", "NO"),
    ]

    concentracion= forms.IntegerField(
        label="Concentración (g/m3)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm','required': 'true' , 'style': 'text-align: center;'}),
        required=True,
    )

    peso= forms.DecimalField(
        decimal_places=1,  
        label="Peso (g)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm','required': 'true' , 'readonly': 'readonly', 'style': 'text-align: center;'}),
        required=True,
    )

    pex= forms.DecimalField(
        decimal_places=1,  
        label= "Pex (bar)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm','required': 'true' , 'style': 'text-align: center;'}),
        required=True,
    )

    pm= forms.DecimalField(
        decimal_places=1,  
        label= "Pm (bar)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm','required': 'true' , 'style': 'text-align: center;'}),
        required=True,
    )

    dpdt= forms.IntegerField(
        label= "dP/dT (bar/s)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm','required': 'true' , 'style': 'text-align: center;'}),
        required=True,
    )

    oxigeno= forms.IntegerField(
        label= "Oxígeno",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm','required': 'true' , 'style': 'text-align: center;'}),
        required=True,
    )

    resultadoPrueba= forms.ChoiceField(
        choices=resultadosPosibles,
        label= "Resultado",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'required': 'true' ,'style': 'text-align: center;'}),
        

    )
    

cloResultadosFormSet= formset_factory(CloResultadosForm, extra=7)


#REC
class RecForm(forms.Form):
    #Todos los campos # se deben establecer en la view
    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    #tiempoEnsayo 


    muestras= Muestras.objects.all()

    
    muestra = forms.ModelChoiceField(
        queryset=muestras,
        label="Muestra",
        empty_label="Selecciona una muestra",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    fechaInicio= forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm',  'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaFin= forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )


    temperaturaAmbiente = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),  # Otras atributos del widget si es necesario
        required=True,
    )

    humedad= forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Humedad Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=True,
    )  

    presion= forms.DecimalField(
        decimal_places=2,
        max_digits=6,
        label="Presión",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    ) 

    observacion=forms.CharField(
        label= "Observación",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

class RecResultadosForm(forms.Form):

    resultadosPosibles=[
        ('', 'Selecciona'),
        ("1", "1"),
        ("2", "2"),
    ]


    nPrueba= forms.ChoiceField(
        choices=resultadosPosibles,
        label= "NumeroPrueba",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'required': 'true' ,'style': 'text-align: center;'}),
    )
    
    tension= forms.IntegerField(
        label="Tensión (V)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;','required': 'required'}),
    )

    tiempo= forms.IntegerField(
        label="Tiempo (s)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'required': 'required'}),

    )

    resultadoPrueba= forms.CharField(
        label= "Resultado (Mohm)",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'required': 'required'}),

    )
    
default_data1 = [
    {'nPrueba': '1', 'tension': 105, 'tiempo': 60, 'resultadoPrueba': 1.23},
    {'nPrueba': '1', 'tension': 500, 'tiempo': 60, 'resultadoPrueba': 1.23},
    {'nPrueba': '1',  'tension': 1000, 'tiempo': 60, 'resultadoPrueba': 1.23},
]

default_data2 = [
    {'nPrueba': '2', 'tension': 105, 'tiempo': 60,},
    {'nPrueba': '2', 'tension': 500, 'tiempo': 60,},
    {'nPrueba': '2',  'tension': 1000, 'tiempo': 60,},
]

recResultadosSerie1FormSet= formset_factory(RecResultadosForm, extra=0)
recResultadosSerie2FormSet= formset_factory(RecResultadosForm, extra=0)

#N1
class N1Form(forms.Form):
    #Todos los campos # se deben establecer en la view
    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    #tiempoEnsayo 

    polvos = [
        ("1", "No metalico"),
        ("2", "Metalico"),
        
    ]

    preseleccion= [
        ("1", "SI"),
        ("2", "NO")
    ]

    muestras= Muestras.objects.all()

    
    muestra = forms.ModelChoiceField(
        queryset=muestras,
        label="Muestra",
        empty_label="Selecciona una muestra",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    fechaInicio= forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm',  'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaFin= forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )


    temperaturaAmbiente = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )

    humedad= forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Humedad Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )  
    
    tipoPolvo= forms.ChoiceField(
        choices= polvos,
        label= "Tipo de polvo",
        widget= forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )

    pruebaPreseleccion= forms.ChoiceField(
        choices= preseleccion,
        label= "Prueba de preselección",
        widget= forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )

    observacion=forms.CharField(
        label= "Observación",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

class N1ResultadosForm(forms.Form):

    rebasa= [
        ("0", "Selecciona"),
        ("1", "SI"),
        ("2", "NO")
    ]

    tiempo= forms.DecimalField(
        decimal_places=2,  
        label="Tiempo (s)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    zonaHumeda= forms.ChoiceField(
        choices=rebasa,
        label="¿Rebasa zona humedecida?", 
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )
    

n1ResultadosFormSet= formset_factory(N1ResultadosForm, extra=7)


#N2
class N2Form(forms.Form):
    #Todos los campos # se deben establecer en la view
    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    #tiempoEnsayo 

    polvos = [
        ("1", "No metalico"),
        ("2", "Metalico"),
        
    ]

    preseleccion= [
        ("1", "SI"),
        ("2", "NO")
    ]

    muestras= Muestras.objects.all()

    
    muestra = forms.ModelChoiceField(
        queryset=muestras,
        label="Muestra",
        empty_label="Selecciona una muestra",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    fechaInicio= forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm',  'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaFin= forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )


    temperaturaAmbiente = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )

    humedad= forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Humedad Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )  
    

    observacion=forms.CharField(
        label= "Observación",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

class N2ResultadosForm(forms.Form):

    resultadosPosibles = [
        ("0", "Seleccione"),
        ("1", "SI"),
        ("2", "NO"),
    ]

    resultado= forms.ChoiceField(
        choices=resultadosPosibles,
        label="Resultado", 
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )
    

n2ResultadosFormSet= formset_factory(N2ResultadosForm, extra=6)



#N4
class N4Form(forms.Form):
    #Todos los campos # se deben establecer en la view
    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    #tiempoEnsayo 

    preseleccion= [
        ("1", "SI"),
        ("2", "NO")
    ]

    muestras= Muestras.objects.all()

    
    muestra = forms.ModelChoiceField(
        queryset=muestras,
        label="Muestra",
        empty_label="Selecciona una muestra",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    fechaInicio= forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm',  'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaFin= forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )


    temperaturaAmbiente = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )

    humedad= forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Humedad Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )  
    

    observacion=forms.CharField(
        label= "Observación",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

class N4ResultadosForm(forms.Form):

    resultadosPosibles = [
        ("0", "Selecciona"),
        ("1", "SI"),
        ("2", "NO"),
    ]

    celdasDisponibles=[
        ("0", "Selecciona"),
        ("1", "25 mm"),
        ("2", "100 mm"),
    ]

    temperaturasDisponibles=[
        ("0", "Selecciona"),
        ("1", "100"),
        ("2", "120"),
        ("3", "140"),
    ]
    celda= forms.ChoiceField(
        choices=celdasDisponibles,
        label="Celda", 
        widget=forms.Select(attrs={'class': 'form-control form-control-sm selects excludeSelect', 'style': 'text-align: center; pointer-events: none; opacity: 0.7;', 'required': 'required'}),
    )

    tConsigna= forms.ChoiceField(
        choices=temperaturasDisponibles,
        label="Temperatura", 
        widget=forms.Select(attrs={'class': 'form-control form-control-sm selects excludeSelect', 'style': 'text-align: center; pointer-events: none; opacity: 0.7;', 'required': 'required'}),
    )

    tMax= forms.DecimalField(
        label="Temperatura máxima", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm inputs', 'style': 'text-align: center;', 'required': 'required'}),
    )

    tiempo= forms.IntegerField(
        label="Tiempo", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm inputs', 'style': 'text-align: center;', 'required': 'required'}),
    )

    resultado= forms.ChoiceField(
        choices=resultadosPosibles,
        label="Resultado", 
        widget=forms.Select(attrs={'class': 'form-control form-control-sm selects', 'style': 'text-align: center;',  'required': 'required'}),
    )
    

n4ResultadosFormSet= formset_factory(N4ResultadosForm, extra=4)


#O1
class O1Form(forms.Form):
    #Todos los campos # se deben establecer en la view
    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")
    #tiempoEnsayo 

    preseleccion= [
        ("1", "SI"),
        ("2", "NO")
    ]

    muestras= Muestras.objects.all()

    
    muestra = forms.ModelChoiceField(
        queryset=muestras,
        label="Muestra",
        empty_label="Selecciona una muestra",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    fechaInicio= forms.DateField(
        label="Fecha Inicio",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm',  'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaFin= forms.DateField(
        label="Fecha Fin",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )


    temperaturaAmbiente = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Otras atributos del widget si es necesario
    )

    humedad= forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Humedad Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )  

    humedadCelulosa = forms.DecimalField(
        decimal_places=2,
        max_digits=3,
        label="Humedad celulosa",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )  
    

    observacion=forms.CharField(
        label= "Observación",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

class O1ResultadosForm(forms.Form):
    ######
    ###### Este form coge los campos de 2 modelos, ResultadosO1 y TiemposO1 ######
    ######

    resultadosPosibles = [
        ("0", "Selecciona"),
        ("1", "SI"),
        ("2", "NO"),
    ]

    porcentajes = [
        ("1", "30/70"),
        ("2", "60/40"),
        ("3", "40/60"),
        ("4", "50/50"),
        ("5", "80/20")
    ]


    proporcion= forms.ChoiceField(
        choices=porcentajes,
        label="Proporción", 
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'readonly':'readonly', 'style': 'text-align: center;'}),
        required=False,
    )


    tiempo1= forms.IntegerField(
        label="T-1", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm tiempo', 'style': 'text-align: center;'}),
        
    )

    tiempo2= forms.IntegerField(
        label="T-2", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm tiempo', 'style': 'text-align: center;'}),
    )

    tiempo3= forms.IntegerField(
        label="T-3", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm tiempo', 'style': 'text-align: center;'}),
    )

    tiempo4= forms.IntegerField(
        label="T-4", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm tiempo', 'style': 'text-align: center;'}),
    )

    tiempo5= forms.IntegerField(
        label="T-5", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm tiempo', 'style': 'text-align: center;'}),
    )

    resultado= forms.FloatField(
        label="Resultado", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly':'readonly', 'style': 'text-align: center;'}),
        
    )
    
o1ResultadosFormSet= formset_factory(O1ResultadosForm, extra=5)



from django import forms
from django.shortcuts import get_object_or_404
from .models import Muestras, Equipos, ListaEnsayos

# Tratamiento
class TratamientoForm(forms.Form):
    preseleccion = [
        ("1", "NO"),
        ("2", "SI")
    ]

    muestra = forms.ModelChoiceField(
        queryset=Muestras.objects.none(),  # Se asignará en __init__
        label="Muestra",
        empty_label="Selecciona una muestra",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    )

    # Secado
    secado = forms.ChoiceField(
        choices=preseleccion,
        label="Secado",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'secado', 'style': 'text-align: center;'})
    )

    equipoSecado = forms.ModelChoiceField(
        queryset=Equipos.objects.none(),
        label="Equipo",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm secado', 'style': 'text-align: center;'})
    )

    fechaSecadoInicio = forms.DateField(
        label="Fecha inicio",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm secado', 'style': 'text-align: center;', 'type': 'date'})
    )

    fechaSecadoFin = forms.DateField(
        label="Fecha fin",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm secado', 'style': 'text-align: center;', 'type': 'date'})
    )

    temperatura = forms.IntegerField(
        label="Temperatura (ºC)",
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm secado', 'style': 'text-align: center;'})
    )

    tiempo = forms.IntegerField(
        label="Tiempo (h)",
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm secado', 'style': 'text-align: center;'})
    )

    # Molienda
    molido = forms.ChoiceField(
        choices=preseleccion,
        label="Molido",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'molido', 'style': 'text-align: center;'})
    )

    equipoMolido = forms.ModelChoiceField(
        queryset=Equipos.objects.none(),
        label="Equipo",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm molido', 'style': 'text-align: center;'})
    )

    fechaMolidoInicio = forms.DateField(
        label="Fecha inicio",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm molido', 'style': 'text-align: center;', 'type': 'date'})
    )

    fechaMolidoFin = forms.DateField(
        label="Fecha fin",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm molido', 'style': 'text-align: center;', 'type': 'date'})
    )

    # Tamizado
    tamizado = forms.ChoiceField(
        choices=preseleccion,
        label="Tamizado",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'tamizado', 'style': 'text-align: center;'})
    )

    equipoTamizado = forms.ModelChoiceField(
        queryset=Equipos.objects.none(),
        label="Equipo",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm tamizado', 'style': 'text-align: center;'})
    )
    
    tamiz = forms.ModelChoiceField(
        queryset=EquipoAsociado.objects.all(),
        label="Tamiz",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm tamizado', 'style': 'text-align: center;'})
    )

    fechaTamizadoInicio = forms.DateField(
        label="Fecha inicio",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm tamizado', 'style': 'text-align: center;', 'type': 'date'})
    )

    fechaTamizadoFin = forms.DateField(
        label="Fecha fin",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm tamizado', 'style': 'text-align: center;', 'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Asignar queryset dinámicamente
        self.fields['muestra'].queryset = Muestras.objects.all()

        # Obtener el ensayo correspondiente
        ensayo = ListaEnsayos.objects.filter(ensayo="Tratamiento").first()

        if ensayo:
            self.fields['equipoSecado'].queryset = Equipos.objects.filter(ensayos=ensayo)
            self.fields['equipoMolido'].queryset = Equipos.objects.filter(ensayos=ensayo)
            self.fields['equipoTamizado'].queryset = Equipos.objects.filter(ensayos=ensayo)

        # Obtener los equipos específicos para tamizado
        """tamiz_tratamiento = Equipos.objects.filter(descripcion="tamices tratamiento").first()
        if tamiz_tratamiento:
            self.fields['equipoTamizado'].queryset = Equipos.objects.filter(equipo_padre=tamiz_tratamiento)"""
