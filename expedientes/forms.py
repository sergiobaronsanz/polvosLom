from django import forms
from .models import Expedientes, Empresa
from muestras.models import ListaEnsayos, Muestras
from django.core.validators import RegexValidator

class ExpedientesForm(forms.Form):
    expediente= forms.CharField(
        label= "Nº Expediente",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
          validators=[RegexValidator(regex=r'^\d{2}\.\d{3}[A-Z]$', message='El número de expediente debe tener el formato XX.XXX seguido de una letra en mayúscula')],
        )
    empresa= forms.CharField(
        label= "Empresa",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center; text-transform: uppercase;'}),
        )
    abreviatura= forms.CharField(
        label= "Abreviatura",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center; text-transform: uppercase;'}),
        required=False
        )
    nMuestras= forms.IntegerField(
        label= "Nº Muestras",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'text-align: center;'}),
        )

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