//Funcion enviar solicitud
function solicitudPOST(datos){  

  // Envía la solicitud POST a la URL de la vista Django
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
        throw new Error(`Error HTTP: ${response.status}`);  // Captura errores HTTP
      }
      return response.json();  // Convierte solo si la respuesta es JSON
    })
    .then(data => {
      console.log('Respuesta del servidor:', data);
    })
    .catch(error => {
      console.error('Error en la solicitud:', error);
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


