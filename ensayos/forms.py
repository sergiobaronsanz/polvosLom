from django import forms
from ensayos.models import Humedad, Granulometria
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
    

    resultado1= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-1", 
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado2= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-2", 
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado3= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-3", 
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado4= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-4", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado5= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-5", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado6= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-6", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado7= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-7", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado8= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-8", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado9= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-9", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado10= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-10", 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
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
        label= "Archivo"

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
        max_digits=5,
        label="Presión",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'})
    ) 


    inductancia= forms.ChoiceField( 
        choices= selecionInductancia,
        label= "Inductancia",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
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

    concentracion= forms.DecimalField(
        decimal_places=2,  
        label="Concentración (g/m3)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    energia= forms.DecimalField(
        decimal_places=2,  
        label="Energía (mJ)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )

    retardo= forms.DecimalField(
        decimal_places=2,  
        label= "Retardo (ms)", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,
    )


    resultadoPrueba= forms.ChoiceField(
        choices=resultadosPosibles,
        label= "Resultado",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        required=False,

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
        decimal_places=2,
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