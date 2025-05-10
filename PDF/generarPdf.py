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
from PyPDF2 import PdfMerger

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
    
    def generate_n1_pdf(self):
        return self.plantilla.N1()
    
    def generate_o1_pdf(self):
        return self.plantilla.O1()
    
    def generate_tratamiento_pdf(self):
        return self.plantilla.tratamiento()
    
    def generate_EmiSin_pdf(self):
        return self.plantilla.emiSin()
    
    def filtroEnsayos(self):
        pdf_files = []
        formateo_pdf_files= []
        nombre_archivo= None
        #Si hay más de un archivo generamos el parte de recepción
        if len(self.request) >1:
                pdf_bytes = self.generate_Recepcion_pdf()
                nombre_archivo= (self.request[0]['muestra_nombre']) + "-" + ("Recepción.pdf")
                pdf_files.append((nombre_archivo, pdf_bytes))
                #Creamos la lista con todos los pdfs pasándolos de binarios a un archivo para poder unirlos (merge)
                formateo_pdf_files.append(io.BytesIO(pdf_bytes))

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
            if request['ensayo'] == 'N1':
                pdf_bytes = self.generate_n1_pdf()
            if request['ensayo'] == 'O1':
                pdf_bytes = self.generate_o1_pdf()
            if request['ensayo'] == 'Tratamiento':
                pdf_bytes = self.generate_tratamiento_pdf()
            if request['ensayo'] == 'EMIsin':
                pdf_bytes = self.generate_EmiSin_pdf()
        
            nombre_archivo= (request['muestra_nombre']) + "-" + (request['ensayo'] + ".pdf")
            # Agregar más tipos de PDF aquí...
            pdf_files.append((nombre_archivo, pdf_bytes))
            #Creamos la lista con todos los pdfs pasándolos de binarios a un archivo para poder unirlos (merge)
            formateo_pdf_files.append(io.BytesIO(pdf_bytes))
        
        return pdf_files, formateo_pdf_files


    # Método principal para gestionar múltiples PDFs
    def generateMuestra(self):
        
        #Sacamos los archivos pdf y el formateo de los mismos para que puedan ser unidos con el merge
        pdf_files, formateo_pdf_files= self.filtroEnsayos()
        
        # Si solo hay un archivo, devolver el PDF directamente
        if len(pdf_files) == 1:
            return pdf_files[0][1]  # Retorna los bytes del PDF
        
        
        # Si hay múltiples archivos, crear un ZIP
        zip_buffer = io.BytesIO()
        output_pdf = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for filename, pdf_data in pdf_files:
                zip_file.writestr(filename, pdf_data)
                
            #Además unificamos todos los pdfs para que en el zip hay un archivo con todos los pdfs
            merger = PdfMerger()
            for pdf in formateo_pdf_files:
                merger.append(pdf) 

            merger.write(output_pdf)
            merger.close()   

            pdfResumen= output_pdf.getvalue()
            zip_file.writestr(f"{self.request[0]['muestra_nombre']}.pdf", pdfResumen)

            
        zip_buffer.seek(0)
        return zip_buffer.getvalue()  # Retorna los bytes del ZIP

    