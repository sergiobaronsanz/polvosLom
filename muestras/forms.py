from django import forms
from .models import DescripcionMuestra, Muestras



class DescripcionMuestraForm(forms.ModelForm):
    class Meta:
        model = DescripcionMuestra
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar las muestras que no tienen una descripción asociada
        self.fields['muestra'].queryset = Muestras.objects.filter(descripcionmuestra__isnull=True)
        
        # Establecer el widget para 'muestra' y darle la clase 'form-control'
        self.fields['muestra'].widget.attrs.update({'class': 'form-control'})

		 # Puedes añadir un widget para personalizar la apariencia de los campos
        
        self.fields['id_fabricante'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['fecha_recepcion'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        self.fields['documentacion'].widget.attrs.update({'class': 'form-control'})
        self.fields['etiquetado'].widget.attrs.update({'class': 'form-control'})
        self.fields['envolturaExt'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['envolturaInt'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['peso'].widget = forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01' })
        self.fields['procedencia'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['estadoEnvio'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['aspectoMuestra'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['color'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['brillo'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['tamano'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['homogeneidad'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['formaEnsayo'].widget.attrs.update({'class': 'form-control'})
        self.fields['observacion'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        self.fields['imagenMuestra'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})
        self.fields['imagenEnvoltorio'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})
        self.fields['usuario'].widget.attrs.update({'class': 'form-control'})

class MuestrasForm(forms.ModelForm):
    class Meta:
        model = Muestras
        exclude = ['fechaRevision']
