from django import forms
from ensayos.models import Humedad
from muestras.models import Muestras
from .models import Equipos
from django.db.models import Q
from django.shortcuts import  get_object_or_404, get_list_or_404


"""
class HumedadForm(forms.ModelForm):
    class Meta:
        model = Humedad
        exclude= ['ensayo']
    #Filtramos para que solo saque las muestras que llevan ensayos de humedad y que además no están ya hecho sdichos ensayos
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar las muestras que no tienen una descripción asociada
        self.fields['muestra'].queryset = Muestras.objects.filter(
            Q(humedad__isnull=True) & Q(listaEnsayos__ensayo__icontains="humedad")
        )
"""
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


class HumedadForm(forms.Form):
    
    muestras= Muestras.objects.filter(
            Q(humedad__isnull=True) & Q(listaEnsayos__ensayo__icontains="humedad")
    )

    criterios= [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('manual', 'Manual'),
    ]

    #Todos los campos # se deben establecer en la view
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
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado2= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-2", 
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
    )

    resultado3= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-3", 
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

    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #desviacion= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Desviación")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo", default=ensayo_humedad)
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")"""
