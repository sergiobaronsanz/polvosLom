from django import forms
from ensayos.models import Humedad
from muestras.models import Muestras
from django.db.models import Q

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


        