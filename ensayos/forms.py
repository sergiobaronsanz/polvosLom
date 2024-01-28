from django import forms
from ensayos.models import Humedad
from muestras.models import Muestras
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
        widget=forms.Select(attrs={'class': 'form-control'})  # Agregar clases CSS si es necesario
    )


    temperaturaAmbiente = forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Temperatura Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control'})  # Otras atributos del widget si es necesario
    )

    humedad= forms.DecimalField(
        decimal_places=2,
        max_digits=5,
        label="Humedad Ambiente",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    criterio= forms.ChoiceField(
        choices=criterios,
        label="Criterio",  # Etiqueta para la opción vacía
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial= "5"
    )

    #Solo si el criterio es manual
    tiempoEnsayo= forms.DecimalField(
        decimal_places=2,  
        label="Tiempo de ensayo", 
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    tDesecacion= forms.IntegerField(
        initial=105, 
        label="Temperatura de Desecación",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    resultado1= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-1", 
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    resultado2= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-2", 
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    resultado3= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-3", 
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    resultado4= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-4", 
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    resultado5= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-5", 
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    resultado6= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-6", 
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    resultado7= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-7", 
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    resultado8= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-8", 
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    resultado9= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-9", 
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    resultado10= forms.DecimalField(
        decimal_places=2,  
        label="Resultado-10", 
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )


    observacion=forms.CharField(
        label= "Observación",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    #ensayo= models.ForeignKey("Humedad", on_delete=models.CASCADE, verbose_name="Ensayo Humedad")
    #desviacion= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Desviación")
    #resultado= models.DecimalField(decimal_places=2, max_digits=5, verbose_name="Resultado")
    #ensayo= models.ForeignKey(ListaEnsayos, on_delete=models.CASCADE, verbose_name="Ensayo", default=ensayo_humedad)
    #equipos= models.ManyToManyField("Equipos", verbose_name="Equipos")"""
