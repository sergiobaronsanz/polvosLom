
from django.shortcuts import render, redirect
from muestras.forms import DescripcionMuestraForm, MuestrasForm

# Create your views here.

"""def seleccionExpediente(request):
    if request.method == 'POST':
        form = MuestrasForm(request.POST)
        if form.is_valid():
            # Guardar el formulario si es válido
            form.save()
            return redirect("/muestras/descripcion")
    else:
        form = MuestrasForm()

    return render(request, 'seleccionExpediente.html', {'form': form})"""

def recepcionMuestra(request):
    if request.method == 'POST':
        print("hola")
        form = DescripcionMuestraForm(request.POST)
        if form.is_valid():
            # Guardar el formulario si es válido
            form.save()
            print("Guardado")
    else:
        form = DescripcionMuestraForm()

    return render(request, 'recepcionMuestra.html', {'form': form})
    