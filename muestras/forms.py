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


class MuestrasForm(forms.ModelForm):
    class Meta:
        model = Muestras
        exclude = ['fechaRevision']
