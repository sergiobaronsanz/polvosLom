'''
Generamos los pdf mediante una clase con una estructura simple:
    Clase para crear el PDF
    Metodo principal para gestionar los pdf
    Metodos para crear cada pdf de los ensayos

'''
import io 
import zipfile
from ensayos.models import *
from muestras.models import *
from .plantillas import PlantillasEnsayo

class PDFGenerator:
    def __init__(self, request):
        self.request= request
        self.plantilla= PlantillasEnsayo(self.request[0]['muestra_id'])
        

    # Métodos para generar diferentes tipos de PDF
    def generate_Recepcion_pdf(self):
        return self.plantilla.recepcion()

    def generate_Humedad_pdf(self):
        return self.plantilla.humedad()

    def generate_Granulometria_pdf(self):
        return self.plantilla.granulometria()
    
    def generate_TMIc_pdf(self):
        return self.plantilla.tmic()

    def generate_TMIn_pdf(self):
        return self.plantilla.tmin()
    
    def generate_LIE_pdf(self):
        return self.plantilla.lie()
    
    def generate_Pmax_pdf(self):
        return self.plantilla.pmax()
    
    def generate_Emi_pdf(self):
        return self.plantilla.emi()
    
    def generate_Rec_pdf(self):
        return self.plantilla.rec()
    
    def generate_Clo_pdf(self):
        return self.plantilla.clo()
    
    def generate_n4_pdf(self):
        return self.plantilla.N4()
    
    def generate_n2_pdf(self):
        return self.plantilla.N2()


    # Método principal para gestionar múltiples PDFs
    def generate(self):
        pdf_files = []
        if len(self.request) >1:
                pdf_bytes = self.generate_Recepcion_pdf()
                nombre_archivo= (self.request[0]['muestra_nombre']) + "-" + ("Recepción.pdf")
                pdf_files.append((nombre_archivo, pdf_bytes))

                print(self.request)

        for request in self.request:
            if request['ensayo'] == 'Humedad':
                pdf_bytes = self.generate_Humedad_pdf()
            if request['ensayo'] == 'Granulometria':
                pdf_bytes = self.generate_Granulometria_pdf()
            if request['ensayo'] == 'TMIc':
                pdf_bytes = self.generate_TMIc_pdf()
            if request['ensayo'] == 'TMIn':
                pdf_bytes = self.generate_TMIn_pdf()
            if request['ensayo'] == 'LIE':
                pdf_bytes = self.generate_LIE_pdf()
            if request['ensayo'] == 'Pmax':
                pdf_bytes = self.generate_Pmax_pdf()
            if request['ensayo'] == 'EMI':
                pdf_bytes = self.generate_Emi_pdf()
            if request['ensayo'] == 'REC':
                pdf_bytes = self.generate_Rec_pdf()
            if request['ensayo'] == 'CLO':
                pdf_bytes = self.generate_Clo_pdf()
            if request['ensayo'] == 'N4':
                pdf_bytes = self.generate_n4_pdf()
            if request['ensayo'] == 'N2':
                pdf_bytes = self.generate_n2_pdf()

        
            nombre_archivo= (request['muestra_nombre']) + "-" + (request['ensayo'] + ".pdf")
            # Agregar más tipos de PDF aquí...
            pdf_files.append((nombre_archivo, pdf_bytes))
        
        # Si solo hay un archivo, devolver el PDF directamente
        if len(pdf_files) == 1:
            return pdf_files[0][1]  # Retorna los bytes del PDF
        
        
        # Si hay múltiples archivos, crear un ZIP
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for filename, pdf_data in pdf_files:
                zip_file.writestr(filename, pdf_data)
        zip_buffer.seek(0)
        return zip_buffer.getvalue()  # Retorna los bytes del ZIP
