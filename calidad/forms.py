from django import forms
from calidad.models import Equipos, EquipoAsociado



class EquiposForm(forms.ModelForm):
    class Meta:
        model = Equipos
        fields = "__all__"
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'equipo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'controlado': forms.CheckboxInput(attrs={"style":"transform: scale(2)"}),
            'ensayos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'fechaCalibracion': forms.TextInput(attrs={'class': 'form-control form-control-sm secado', 'style': 'text-align: center;', 'type': 'date'}),
            'fechaCaducidadCalibracion': forms.TextInput(attrs={'class': 'form-control form-control-sm secado', 'style': 'text-align: center;', 'type': 'date'}),
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


class EquiposAsociadosForm(forms.ModelForm):
    class Meta:
        model= EquipoAsociado
        exclude = ['equipoAsociado']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'equipo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }
         