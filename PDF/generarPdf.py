'''
Generamos los pdf mediante una clase con una estructura simple:
    Clase para crear el PDF
    Metodo principal para gestionar los pdf
    Metodos para crear cada pdf de los ensayos

'''
import io
from fpdf import FPDF  # o reportlab
import zipfile
from ensayos.models import *
from muestras.models import *
import os

class PDFGenerator:
    def __init__(self):
        self.rutaAbsoluta = os.path.dirname(__file__)

    # Métodos para generar diferentes tipos de PDF
    def generate_TMIc_pdf(self, muestra):
        muestra= Muestras.objects.get(id= muestra)
        descripcion= DescripcionMuestra.objects.get(muestra=muestra)
        ensayo= TMIc.objects.get(muestra= muestra)
        equipos=ensayo.equipos.all()
        resultados= ResultadosTMIc.objects.filter(ensayo= ensayo).order_by("id")
        ensayoForma= descripcion.get_formaEnsayo_display()
        fecha= ensayo.fecha
        identificacion= f"{muestra.empresa.abreviatura} - {muestra.id_muestra}"

        
        pdf = FPDF(orientation = 'P', unit= 'mm', format = 'A4')
        pdf.add_page()
        

        #TEXTO 
        pdf.set_font('Arial', '', 12)
        #IMAGEN
        pdf.image(self.rutaAbsoluta + '/Imagenes/LOGO.png', x=8, y= 8, w=30, h=30, link="http://www.lom.upm.es")

        #Celdas Cabecera
        pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        pdf.cell(w= 100, h= 12, txt = ensayo.ensayo.ensayo, border= 1, 
                align= "C", fill = 0)
        pdf.multi_cell(w=0, h= 12, txt = "Fecha:", border= "RT", 
                align= "L", fill = 0)

        pdf.cell(w=35, h= 12,border= 0,
                align= "C", fill = 0)
        pdf.cell(w=100, h= 12, txt = ensayo.ensayo.normativa,border= "LRB", 
                align= "C", fill = 0)
        pdf.multi_cell(w=0, h= 12, txt = fecha.strftime("%d/%m/%Y"), border= "RB", 
                align= "C", fill = 0)

        #Celda I/D muestra
        pdf.multi_cell(w=0, h= 5,border= 0,
                align= "C", fill = 0)
        pdf.cell(w=130, h= 8,border= 0, txt= f"Material: {descripcion.id_fabricante}",
                align= "J", fill = 0)
        pdf.multi_cell(w=60, h= 8,border= 0, txt= f"Identificación: {identificacion}",
                align= "J", fill = 0)

        #Celda Tratamiento de muestras  
        pdf.set_font('Arial', 'B', 12) 
        pdf.cell(w=65, h= 8,border= "LT", txt= "MUESTRA DE POLVO",
                align= "J", fill = 0)

        pdf.set_font('Arial', '', 12)    
        pdf.multi_cell(w=125, h= 8,border= "TR", txt= f"La muestra se ensaya {ensayoForma}",
                align= "J", fill = 0)


        #Celda Condiciones ambientales  
        pdf.set_font('Arial', 'B', 12) 
        pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "CONDICIONES AMBIENTALES",
                align= "J", fill = 0)

        pdf.set_font('Arial', '', 12)    
        pdf.cell(w=95, h= 8,border= "L", txt= f"Temperatura: {ensayo.temperaturaAmbiente} ºC",
                align= "C", fill = 0)

        pdf.multi_cell(w=95, h= 8,border= "R", txt= f"Humedad: {ensayo.humedad} %",
                align= "C", fill = 0)


        #Celda Equipos
        pdf.set_font('Arial', 'B', 12) 
        pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "EQUIPOS DE ENSAYO",
                align= "J", fill = 0)
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(w=190, h= 8,border= "LBR", txt = "Equipos: " + " | ".join(equipo.codigo for equipo in equipos),###
                align= "J", fill = 0)



        #Celda Procedimiento
        pdf.set_font('Arial', 'B', 12) 
        pdf.multi_cell(w=190, h= 8,border= "LR", txt= "PROCEDIMIENTO",
                align= "J", fill = 0)
        #Leyenda superior
        pdf.cell(w=5, h= 8,border= "L", fill = 0)    
        pdf.set_font('Arial', '', 12)
        pdf.cell(w=60, h= 8,border= "LT", txt= "Incrementos Tª 10 K", fill = 0)
        pdf.cell(w=45, h= 8,border= "T", txt= "Altura capa: 5 mm",fill = 0)
        pdf.cell(w=75, h= 8,border= "TR",txt= "Volumen (h=5, r=50)= 39,27 cm3", fill = 0)
        pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)
        
        #Parámetros tabla
        pdf.cell(w=5, h= 8,border= "L", fill = 0)
        pdf.cell(w=29, h= 8,border= 1,align= "C", 
                txt= "Tª Plato", fill = 0)
        pdf.cell(w=29, h= 8,border= 1,align= "C", 
                txt= "Tª Max", fill = 0)
        pdf.cell(w=24, h= 8,border= 1,align= "C", 
                txt= "¿Ignición?", fill = 0)
        pdf.cell(w=40, h= 8,border= 1, align= "C",
                txt= "Visual/termopar", fill = 0)
        pdf.cell(w=29, h= 8,border= 1, align= "C",
                txt= "Tiempo TªMax", fill = 0)
        pdf.cell(w=29, h= 8,border= 1, align= "C",
                txt= "Tiempo", fill = 0)

        pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)

        #Resultados tabla (Habría que incluir esto en una clase con las variables)
        for fila in resultados:
            print(fila)
        for fila in resultados:
            pdf.cell(w=5, h= 8,border= "L", fill = 0)
            pdf.cell(w=29, h= 8,border= 1,align= "C",txt= str(int(fila.tPlato)), 
                    fill = 0)
            pdf.cell(w=29, h= 8,border= 1,align= "C",txt= str(int(fila.tMaxima)),
                    fill = 0)
            pdf.cell(w=24, h= 8,border= 1,align= "C",txt= fila.get_resultado_display(),
                    fill = 0)
            pdf.cell(w=40, h= 8,border= 1, align= "C",txt= fila.get_tipoIgnicion_display(),
                    fill = 0)
            pdf.cell(w=29, h= 8,border= 1, align= "C",txt= str(int(fila.tiempoTmax)),
                    fill = 0)
            pdf.cell(w=29, h= 8,border= 1, align= "C",txt= str(int(fila.tiempoPrueba)),
                    fill = 0)
            pdf.multi_cell(w=5, h= 8,border= "R", fill = 0)
        
        try:
            ti= int(ensayo.resultado)
            ta= int(ensayo.resultado) - 10
        except:
            ti= ensayo.resultado
            ta= "N/D"

        #Celda con Resultados
        pdf.multi_cell(w=190, h= 5,border= "LR", fill = 0)
        pdf.set_font('Arial', 'B', 12) 
        pdf.multi_cell(w=190, h= 8,border= "LRT", txt= "RESULTADOS",
                align= "J", fill = 0)
        pdf.set_font('Arial', '', 12) 
        
        if ti == ">400":
            pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Menor temperatura a la que se produce ignición:     {ti} ºC* ",
                    align= "J", fill = 0)
        else:
            pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Menor temperatura a la que se produce ignición:     {str(ti)} ºC* ",
                    align= "J", fill = 0)

        pdf.multi_cell(w=190, h= 8,border= "LR", txt= f"Mayor temperatura a la que no se produce ignición:     {ta} ºC ",
                align= "J", fill = 0)

        #Celda resultado final       
        pdf.set_font('Arial', 'B', 14) 
        if ti == ">400":
            pdf.multi_cell(w=190, h= 8,border= 1, txt= f"TEMPERATURA MÍNIMA DE IGNICIÓN EN CAPA:     {ti} ºC ",
                    align= "C", fill = 0)
        else:
            pdf.multi_cell(w=190, h= 8,border= 1, txt= f"TEMPERATURA MÍNIMA DE IGNICIÓN EN CAPA:     {str(ti)} ºC ",
                    align= "C", fill = 0)
        #Firma
        pdf.set_font('Arial', '', 14) 
        pdf.cell(w=95, h= 8,border= 1, txt= f"Conforme:",
                align= "J", fill = 0)
        pdf.multi_cell(w=95, h= 8,border= 1, txt= f"Realizado: SBS",###
                align= "J", fill = 0)
        
        # Agregar más contenido dinámico aquí...
        return pdf.output(dest='S').encode('latin1')  # Devuelve bytes

    def generate_TMIn_pdf(self, muestra):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Reporte: {muestra}", ln=True)
        # Agregar más contenido dinámico aquí...
        return pdf.output(dest='S').encode('latin1')  # Devuelve bytes

    # Método principal para gestionar múltiples PDFs
    def generate(self, pdf_requests):
        pdf_files = []

        for request in pdf_requests:
            if request['ensayo'] == 'TMIc':
                pdf_bytes = self.generate_TMIc_pdf(request['muestra_id'])
            elif request['ensayo'] == 'TMIn':
                pdf_bytes = self.generate_TMIn_pdf(request['muestra_id'])
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

"""# Ejemplo de uso
pdf_gen = PDFGenerator()
pdf_requests = [
    {'type': 'invoice', 'data': {'invoice_number': '12345'}, 'filename': 'factura_12345.pdf'},
    {'type': 'report', 'data': {'title': 'Ventas 2024'}, 'filename': 'reporte_ventas.pdf'}
]
output = pdf_gen.generate(pdf_requests)

# Guardar el resultado según la cantidad de archivos
with open('output.zip' if len(pdf_requests) > 1 else 'output.pdf', 'wb') as f:
    f.write(output)"""
