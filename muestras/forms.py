from django import forms
from .models import DescripcionMuestra, Muestras



class DescripcionMuestraForm(forms.ModelForm):
    class Meta:
        model = DescripcionMuestra
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        
        # Hacer todos los campos obligatorios
        for field_name, field in self.fields.items():
            if field_name != 'imagenEnvoltorio':  # esta será opcional
                field.required = True
            else:
                field.required = False
        
        self.fields['muestra'].widget.attrs.update({'class': 'form-control'})        
        self.fields['id_fabricante'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['fecha_recepcion'].widget = forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        self.fields['empresaTransporte'].widget = forms.TextInput(attrs={'class': 'form-control'})
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
        self.fields['humedadAparente'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['formaEnsayo'].widget.attrs.update({'class': 'form-control'})
        self.fields['observacion'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        self.fields['imagenMuestra'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})
        self.fields['imagenEnvoltorio'].widget = forms.ClearableFileInput(attrs={'class': 'form-control'})
        self.fields['usuario'].widget.attrs.update({'class': 'form-control'})

class MuestrasForm(forms.ModelForm):
    class Meta:
        model = Muestras
        exclude = ['fechaRevision']
