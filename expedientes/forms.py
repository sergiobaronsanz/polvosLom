from django import forms
from .models import Expedientes, Empresa
from muestras.models import ListaEnsayos, Muestras

class ExpedientesForm(forms.Form):
    expediente= forms.CharField(label="Nº expediente")
    empresa= forms.CharField(label= "Empresa")
    abreviatura= forms.CharField(label= "Abreviatura", required=False)
    nMuestras= forms.IntegerField(label= "Numero de muestras")

class listaEnsayosForm(forms.ModelForm):
    class Meta:
        model = ListaEnsayos
        exclude = ['fechaRevision']
    
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        exclude = ['fechaRevision']
        
class EnsayosMuestras(forms.ModelForm):
    class Meta:
        model = Muestras
        fields = ['listaEnsayos', 'observaciones']
        widgets = {
            'listaEnsayos': forms.CheckboxSelectMultiple
        }