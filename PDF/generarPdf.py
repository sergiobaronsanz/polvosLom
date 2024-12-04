'''
Generamos los pdf mediante una clase con una estructura simple:
    Clase para crear el PDF
    Metodo principal para gestionar los pdf
    Metodos para crear cada pdf de los ensayos

'''
import io
from fpdf import FPDF  # o reportlab
import zipfile

class PDFGenerator:
    def __init__(self):
        pass

    # Métodos para generar diferentes tipos de PDF
    def generate_TMIc_pdf(self, muestra):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Factura: {muestra}", ln=True)
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
