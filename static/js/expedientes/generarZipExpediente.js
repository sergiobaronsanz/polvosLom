function solicitudPOSTzip(datos) {  
  fetch('/expedientes/ver-expedientes/generarZip', {
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
    if (contentType === 'application/zip') {
      return response.blob().then(blob => {
        // Crear una URL temporal para descargar el archivo
        const url = window.URL.createObjectURL(blob);

        // Extraer el nombre del archivo del header
        const contentDisposition = response.headers.get('Content-Disposition');
        const filename = contentDisposition
          ? contentDisposition.split('filename=')[1].replace(/"/g, '')
          : 'archivo.zip'; // Si no se obtiene nombre, asignar 'archivo.zip'

        // Crear un enlace para descargar el archivo
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();

        // Liberar memoria
        window.URL.revokeObjectURL(url);

        console.log('Archivo descargado correctamente');
        
        // Mostrar modal de éxito
        var myModal = new bootstrap.Modal(document.getElementById('archivoGuardado'));
        myModal.show();  
      });
    } else {
      return response.json().then(data => {
        // Aquí puedes manejar los errores enviados como JSON (por ejemplo, un mensaje de error)
        console.log('Error en la respuesta:', data);
        var myModal = new bootstrap.Modal(document.getElementById('errorArchivoGuardado'));
        myModal.show();
      });
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
  botonZIP= document.getElementById("generarZipExpediente");
  
	//Generar Zip
  botonZIP.addEventListener("click", function() {
	console.log('Generando archivo ZIP...');
	let datos = [];
	ensayosMuestras.forEach(element => {
	  datos.push(element)
	});
  
	console.log(datos)
  
	solicitudPOSTzip(datos);  // Llamamos a la función de solicitud POST
  });
  
  
  
  