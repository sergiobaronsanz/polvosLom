
// Configurar la ubicación del trabajador
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js';

// Asegurarse de que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('id_archivo');
    const resultElement = document.getElementById('result');

    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];

        if (file && file.type === 'application/pdf') {
            const reader = new FileReader();
            reader.onload = function(e) {
                const arrayBuffer = e.target.result;
                const uint8Array = new Uint8Array(arrayBuffer);
                
                // Cargar el PDF con pdf.js
                pdfjsLib.getDocument(uint8Array).promise.then(function(pdf) {
                    pdf.getPage(1).then(function(page) {
                        page.getTextContent().then(function(textContent) {
                            const text = textContent.items.map(item => item.str).join(' ');
                            if (resultElement) {
                                resultElement.textContent = text;
                            } else {
                                console.error('Elemento result no encontrado');
                            }
                        }).catch(function(error) {
                            console.error('Error al obtener el texto de la página:', error);
                        });
                    }).catch(function(error) {
                        console.error('Error al obtener la página:', error);
                    });
                }).catch(function(error) {
                    console.error('Error al cargar el documento PDF:', error);
                });
            };
            reader.readAsArrayBuffer(file);
        } else {
            if (resultElement) {
                resultElement.textContent = 'Por favor selecciona un archivo PDF.';
            }
        }
    });
});