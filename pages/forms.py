from django import forms
from datetime import datetime

class ReporteForm (forms.Form):
    fechaInicio = forms.DateField(
        label="Fecha incio",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm col', 'style': 'text-align: center;', 'type': 'date'})
    )

    fechaFin = forms.DateField(
        label="Fecha fin",
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control form-control-sm col', 'style': 'text-align: center;', 'type': 'date'})
    )

    fechaYear= forms.IntegerField(
        label= "Año",
        initial= datetime.now().year,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm col', 'style': 'text-align: center;',})
    )

