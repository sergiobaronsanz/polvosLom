//Funcion envío de mail
botonEnvioMail= document.getElementById("sendMail");

botonEnvioMail.addEventListener("click", function(){
    emails= document.querySelectorAll(".emails");
    emails.forEach(element => {
        console.log(element.textContent);
    });

    datos=[
      {"expediente": expediente},
      {"listaEmails" : listaEmails},
    ];
    console.log("Enviamos el correo");

    fetch('/expedientes/envioMail', {
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
  })