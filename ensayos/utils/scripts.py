#Scripts de ayuda
import PyPDF2
import re

#Leer pdf de granulometria

class LecturaGranulometria:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extraer_valor(self, key):
        try:
            # Abrir el archivo PDF
            with open(self.pdf_path, 'rb') as archivo:
                lector_pdf = PyPDF2.PdfFileReader(archivo)
                num_paginas = lector_pdf.numPages
                texto_completo = ''

                # Leer el contenido de cada página
                for i in range(num_paginas):
                    pagina = lector_pdf.getPage(i)
                    texto_completo += pagina.extract_text() + '\n'

                # Buscar la palabra clave y el número que le sigue
                patron = rf'{key}\s*=\s*(\d+)'  # Patrón de búsqueda
                coincidencia = re.search(patron, texto_completo)

                if coincidencia:
                    return coincidencia.group(1)  # Devuelve el número encontrado
                else:
                    return f'No se encontró "{key}" en el PDF.'
        except Exception as e:
            return str(e)

# Ejemplo de uso
if __name__ == "__main__":
    # Ruta al archivo PDF y palabra clave
    ruta_archivo_pdf = 'archivo.pdf'
    palabra_clave = 'd10'

    # Crear una instancia de la clase y extraer el valor
    lector = LecturaGranulometria(ruta_archivo_pdf)
    valor = lector.extraer_valor(palabra_clave)
    print(f'El valor de {palabra_clave} es: {valor}')
