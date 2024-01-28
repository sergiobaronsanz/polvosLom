from django.shortcuts import render
from .forms import HumedadForm

# Create your views here.
def humedad(request):
    form = HumedadForm()

    if request.method == 'POST':
        form = HumedadForm(request.POST)

        if form.is_valid():  # Corregir aquí
            print("El formulario es válido")
            # Realizar acciones con los datos del formulario si es válido

    return render(request, 'humedad.html', {
        'form': form
    })