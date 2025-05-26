//Funcion enviar solicitud
// Función para enviar solicitud POST y manejar la descarga del archivo
// Función para enviar solicitud POST y manejar la descarga del archivo
function solicitudPOST(datos) {  

  fetch('/ensayos/generarPdf', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(datos)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`);
    }
    const contentType = response.headers.get('Content-Type');
    if (contentType === 'application/pdf' || contentType === 'application/zip') {
      return response.blob().then(blob => {
        // 🔹 Crear una URL temporal para descargar
        const url = window.URL.createObjectURL(blob);

        // 🔹 Extraer el nombre del archivo del header
        const contentDisposition = response.headers.get('Content-Disposition');
        const filename = contentDisposition
          ? contentDisposition.split('filename=')[1].replace(/"/g, '')
          : 'archivo.pdf';

        // 🔹 Crear un enlace para descargar el archivo
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();

        // 🔹 Liberar memoria
        window.URL.revokeObjectURL(url);

        console.log('Archivo descargado correctamente');
        var myModal = new bootstrap.Modal(document.getElementById('archivoGuardado'));
        myModal.show();  
      });
    } else {
      return response.json(); // ← Si es un error del servidor, lo manejamos como JSON
    }
  })
  .then(data => {
    if (data && !(data instanceof Blob)) {
      console.log('Respuesta del servidor:', data);
    }
  })
  .catch(error => {
    console.error('Error en la solicitud:', error);
    var myModal = new bootstrap.Modal(document.getElementById('errorArchivoGuardado'));
    myModal.show();
  });

  // Función para obtener el CSRF token de las cookies (necesaria en Django)
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
}



///Generar archivos
botonZIP= document.getElementById("generarZip");
botonPDF= document.getElementById("generarPdf");
ensayoElegido= document.getElementById("ensayoElegido");
console.log(ensayos);
console.log(muestra);

  //Generar Zip
botonZIP.addEventListener("click", function() {
  console.log('Generando archivo ZIP...');
  let datos = [];
  ensayos.forEach(element => {
    datos.push(element)
  });

  console.log(datos)

  solicitudPOST(datos);  // Llamamos a la función de solicitud POST
});

  //Generar pdf
botonPDF.addEventListener("click", function(){
    console.log("hola amigo");
    const saveChangesBtn = document.getElementById("saveChangesBtn");
    const checklistForm = document.getElementById("checklistForm");

    saveChangesBtn.addEventListener("click", function () {
      // Obtener el valor seleccionado del formulario
      const formData = new FormData(checklistForm);
      const selectedValue = formData.get("ensayo");

      if (selectedValue) {
        console.log("Valor seleccionado:", selectedValue);
        // Aquí puedes enviar los datos al servidor con fetch o realizar otra acción
        ensayos.forEach(element=>{
          if (element.ensayo === selectedValue){
            let datos= [];
            datos.push(element);
            console.log(datos);
            solicitudPOST(datos);
            
          }
        });

      } else {
        alert("Por favor, selecciona una opción.");
      }
    });
  });


