function solicitudPOSTzip(datos){  

	// Envía la solicitud POST a la URL de la vista Django
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
		  throw new Error(`Error HTTP: ${response.status}`);  // Captura errores HTTP
		}
		return response.json();  // Convierte solo si la respuesta es JSON
	  })
	  .then(data => {
		console.log('Respuesta del servidor:', data);
		/*var myModal = new bootstrap.Modal(document.getElementById('archivoGuardado'));
		myModal.show();	*/
	  })
	  .catch(error => {
		console.error('Error en la solicitud:', error);
		/*var myModal = new bootstrap.Modal(document.getElementById('errorArchivoGuardado'));
		myModal.show();*/
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
  
  
  
  