from django import forms
from ensayos.models import Humedad, Granulometria 
from muestras.models import ListaEnsayos
from muestras.models import Muestras
from .models import Equipos
from django.db.models import Q
from django.shortcuts import  get_object_or_404, get_list_or_404
from django.forms import formset_factory


class EquiposForm(forms.ModelForm):
    class Meta:
        model = Equipos
        fields = "__all__"
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'equipo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'ensayos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'fechaCalibracion': forms.TextInput(attrs={'class': 'form-control'}),
            'fechaCaducidadCalibracion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EquiposEnsayoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí se establece dinámicamente el queryset
        self.fields['equiposEnsayo'].queryset = Equipos.objects.all()

    equiposEnsayo=forms.ModelMultipleChoiceField(
        queryset=Equipos.objects.none(),
        label="Equipos",
        widget=forms.SelectMultiple(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )


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
    
    fecha= forms.DateField(
        label="Fecha",
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
    
    fecha= forms.DateField(
        label="Fecha",
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
    
    fecha= forms.DateField(
        label="Fecha",
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

    tiempoMaxEnsayo=forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label= "Tiempo máximo del ensayo",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    funde= forms.ChoiceField(
        choices=funde_muestra,
        label= "Tipo ignición",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
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

    tPlato= forms.DecimalField(
        decimal_places=2,  
        label="Temperatura Plato (ºC)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
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

    tiempoPrueba= forms.DecimalField(
        decimal_places= 2,
        label= "Tiempo total (min)",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,

    )

    tiempoMax= forms.DecimalField(
        decimal_places= 2,
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
    
    fecha= forms.DateField(
        label="Fecha",
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

class TminResultadosForm(forms.Form):
    resultadosPosibles=[
        ('', 'Selecciona'),
        ("1", "SI"),
        ("2", "NO"),
    ]

    tHorno= forms.DecimalField(
        decimal_places=2,  
        label="Temperatura Horno (ºC)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    peso= forms.DecimalField(
        decimal_places=2,  
        label="Peso (g)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    presion= forms.DecimalField(
        decimal_places=2,  
        label= "Presion (kPa)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    resultadoPrueba= forms.ChoiceField(
        choices=resultadosPosibles,
        label= "Resultado",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
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
    
    fecha= forms.DateField(
        label="Fecha",
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
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    peso= forms.DecimalField(
        decimal_places=2,  
        label="Peso (g)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly': 'readonly', 'style': 'text-align: center;'}),
        required=False,
    )

    pex= forms.DecimalField(
        decimal_places=2,  
        label= "Pex (bar)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    pm= forms.DecimalField(
        decimal_places=2,  
        label= "Pm (bar)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    dpdt= forms.DecimalField(
        decimal_places=2,  
        label= "dP/dT (bar/s)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    resultadoPrueba= forms.ChoiceField(
        choices=resultadosPosibles,
        label= "Resultado",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
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
    
    fecha= forms.DateField(
        label="Fecha",
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

    resultado= forms.IntegerField(
        label="Resultado (Es)",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=True,
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
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm resultadosPruebas', 'style': 'text-align: center;'}),
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
        ("1", "simex"),
        ("2", "sobbe"),
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
    
    fecha= forms.DateField(
        label="Fecha",
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

    concentracion= forms.DecimalField(
        decimal_places=2,  
        label="Concentración (g/m3)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    peso= forms.DecimalField(
        decimal_places=2,  
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
        decimal_places=2,  
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
    
    fecha= forms.DateField(
        label="Fecha",
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

    concentracion= forms.DecimalField(
        decimal_places=2,  
        label="Concentración (g/m3)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    peso= forms.DecimalField(
        decimal_places=2,  
        label="Peso (g)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'readonly': 'readonly', 'style': 'text-align: center;'}),
        required=False,
    )

    pex= forms.DecimalField(
        decimal_places=2,  
        label= "Pex (bar)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    pm= forms.DecimalField(
        decimal_places=2,  
        label= "Pm (bar)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    dpdt= forms.DecimalField(
        decimal_places=2,  
        label= "dP/dT (bar/s)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    oxigeno= forms.IntegerField(
        label= "Oxígeno",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    resultadoPrueba= forms.ChoiceField(
        choices=resultadosPosibles,
        label= "Resultado",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,

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
    
    fecha= forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'type': 'date'}),  # Otras atributos del widget si es necesario
        required=True,
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

    observacion=forms.CharField(
        label= "Observación",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

class RecResultadosForm(forms.Form):

    tension= forms.IntegerField(
        label="Tensión (V)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;','required': 'required'}),
    )

    tiempo= forms.IntegerField(
        label="Tiempo (s)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'required': 'required'}),

    )

    resultadoPrueba= forms.DecimalField(
        decimal_places=2,
        max_digits= 8,
        label= "Resultado (Mohm)",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;', 'required': 'required'}),

    )
    

recResultadosFormSet= formset_factory(RecResultadosForm, extra=7)


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
    
    fecha= forms.DateField(
        label="Fecha",
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
    
    fecha= forms.DateField(
        label="Fecha",
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
    
    fecha= forms.DateField(
        label="Fecha",
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
        required=False,
    )

    tConsigna= forms.ChoiceField(
        choices=temperaturasDisponibles,
        label="Temperatura", 
        widget=forms.Select(attrs={'class': 'form-control form-control-sm selects excludeSelect', 'style': 'text-align: center; pointer-events: none; opacity: 0.7;', 'required': 'required'}),
        required=False,
    )

    tMax= forms.DecimalField(
        label="Temperatura máxima", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm inputs', 'style': 'text-align: center;', 'required': 'required'}),
        required=False,
    )

    tiempo= forms.IntegerField(
        label="Tiempo", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm inputs', 'style': 'text-align: center;', 'required': 'required'}),
        required=False,
    )

    resultado= forms.ChoiceField(
        choices=resultadosPosibles,
        label="Resultado", 
        widget=forms.Select(attrs={'class': 'form-control form-control-sm selects', 'style': 'text-align: center;',  'required': 'required'}),
        required=False,
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
    
    fecha= forms.DateField(
        label="Fecha",
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


#Tratamiento
class tratamientoForm(forms.Form):

    preseleccion= [
        ("1", "NO"),
        ("2", "SI")
        
    ]

    tamices= [
        ("0", ""),
        ("1", "500"),
        ("2", "1000"),
        ("2", "250"),
        ("2", "800"),
        ("2", "125"),
        ("2", "63"),
    ]

    muestras= Muestras.objects.all()


    ensayo= get_object_or_404(ListaEnsayos, ensayo= "Tratamiento")
    equipos= Equipos.objects.filter(ensayos= ensayo)
    tamizTratamiento= Equipos.objects.filter(descripcion= "tamices tratamiento") #Hay que incluir tamices tratamiento en la descripcion del equipo
    equiposTamizado= Equipos.objects.filter(equipo_padre= tamizTratamiento[0])

    print(f"Los equipos son {equipos}")


    
    muestra = forms.ModelChoiceField(
        queryset=muestras,
        label="Muestra",
        empty_label="Selecciona una muestra",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    #Secado
    secado = forms.ChoiceField(
        choices=preseleccion,
        label="Secado",
        required=True,
         # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'secado', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )

    equipoSecado = forms.ModelChoiceField(
        queryset=equipos,
        label="Equipo",
        required=False,
         # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm secado', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )

    fechaSecadoInicio= forms.DateField(
        label="Fecha inicio",
		required=False,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm secado', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaSecadoFin= forms.DateField(
        label="Fecha fin",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm secado', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    temperatura= forms.IntegerField(
        label="Temperatura (ºC)",
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm secado', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
    tiempo=forms.IntegerField(
        label="Tiempo (h)",
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm secado', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )
    
        

    #Molienda
    molido = forms.ChoiceField(
        choices=preseleccion,
        label="Molido",
        required=True,
         # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'molido', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )

    equipoMolido = forms.ModelChoiceField(
        queryset= equipos,
        label="Equipo",
        required=False,
         # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm molido', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )

    fechaMolidoInicio= forms.DateField(
        label="Fecha inicio",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm molido', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaMolidoFin= forms.DateField(
        label="Fecha fin",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm molido', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    #Tamizado
    tamizado = forms.ChoiceField(
        choices=preseleccion,
        label="Tamizado",
        required=True,
         # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm','id': 'tamizado', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )


    equipoTamizado = forms.ModelChoiceField(
        queryset= equiposTamizado,
        label="Equipo",
        required=False,
         # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control form-control-sm tamizado', 'style': 'text-align: center;'})  # Agregar clases CSS si es necesario
    )

    fechaTamizadoInicio= forms.DateField(
        label="Fecha inicio",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm tamizado', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )

    fechaTamizadoFin= forms.DateField(
        label="Fecha fin",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm tamizado', 'style': 'text-align: center;', 'type': 'date'})  # Otras atributos del widget si es necesario
    )
