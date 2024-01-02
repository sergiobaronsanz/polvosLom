from django.test import TestCase
from muestras.models import *
from ensayos.models import *
from expedientes.models import *

# Create your tests here.
class prueba(TestCase):
    def prueba(self):
        ensayo= ListaEnsayos(ensayo= "TMIn", normativa= "UNE-EN ISO/IEC 80079-20-2:2016", poens= "552")
        ensayo.save()
        
        ensayos= ListaEnsayos.objects.all()
        print(ensayos)
        

# Crear una instancia de la clase de prueba y llamar al método
prueba_instance = prueba()
prueba_instance.prueba()
