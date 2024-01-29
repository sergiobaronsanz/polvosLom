from django.shortcuts import render
from .forms import HumedadForm

# Create your views here.
def humedad(request):
    form = HumedadForm()
    
    #Aquí van los campos que queremos ocultar del formulario
    camposOcultos= []
    for i in range(4,11):
        camposOcultos.append(f"resultado{i}")

    if request.method == 'POST':
        form = HumedadForm(request.POST)

        if form.is_valid():  # Corregir aquí
            print("El formulario es válido")
            # Realizar acciones con los datos del formulario si es válido

    return render(request, 'ensayos/humedad.html', {
        'form': form,
        'camposOcultos': camposOcultos,
    })