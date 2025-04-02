from django.shortcuts import render, redirect
from .forms import *


# Create your views here.
#Equipos
def equipos (request):
    equipos= Equipos.objects.all().order_by()
    print("holaaaaaaaaaaaaaaaaaaaaaaaa")
    
    return render (request, "equipos/equipos.html",{
        'equipos': equipos
        
    })
    
def nuevoEquipo (request):
    if request.method == "POST":
        form= EquiposForm(request.POST)
        
        if form.is_valid():
            form.save()

            return redirect ("equipos")
               
    else:
        form= EquiposForm()
    
    return render (request, "equipos/nuevoEquipo.html",{
        'equipos': equipos,
        'form': EquiposForm,
        
    })
