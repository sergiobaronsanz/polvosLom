from django.shortcuts import render
from .forms import HumedadForm

# Create your views here.
def humedad(request):
    form= HumedadForm()

    return render (request, 'humedad.html', {
        'form': form
        
    })