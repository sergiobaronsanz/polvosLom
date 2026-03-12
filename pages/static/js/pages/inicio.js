//Incio.js
document.addEventListener("DOMContentLoaded", () => {
    console.log("inicio bien ");

    //Variables globales
        let inicio= document.getElementById("id_fechaInicio");
        let fin= document.getElementById("id_fechaFin");
        let year= document.getElementById("id_fechaYear");


    //Cambio periodo
    function cambioPeriodo(){
        let selectorPeriodo= document.getElementById("tipoPeriodo");
        let campoInicio= document.getElementById("fechaInicio");
        let campoFin= document.getElementById("fechaFin");
        let campoYear= document.getElementById("fechaYear");

        campoYear.style.display= "none";
        let año= year.value;
        year.value=0;

        selectorPeriodo.addEventListener("change", (e)=>{
            console.log("Hola");
            if (e.target.value === "1"){
                campoInicio.style.display= "flex";
                campoFin.style.display= "flex";
                campoYear.style.display= "none";
                year.value=0;
            }

            if (e.target.value === "2"){
                campoInicio.style.display= "none";
                inicio.value=0;
                campoFin.style.display= "none";
                fin.value=0;
                campoYear.style.display= "flex";
                year.value=año;

            }
        })

    };


    //Envio de formulario
    function envioFormulario(){
        botonEnvio= document.getElementById("generarReporte");

        botonEnvio.addEventListener("click",function(){
            let datos = {
                "fechaInicio": inicio.value,
                "fechaFin": fin.value,
                "fechaYear": year.value
            };
            console.log(datos);

            fetch('/reporte/',{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(datos)

            })
            .then(response =>{
                if (!response.ok) {
                    throw new Error(`Error HTTP: ${response.status}`);  // Captura errores HTTP
                }
                const contentType = response.headers.get('Content-Type');
                if (contentType === 'application/pdf') {
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
                console.log('Respuesta del servidor:', data);
                console.log(data);
                if (data.mensaje === "Email enviado") {
                    $('#seleccionReporte').modal('hide');   // 👈 Cierra el modal
                    //$('#emailEnviado').modal('show');
                }
            })
            .catch(error => {
                console.error('Error en la solicitud:', error);
                $('#modalMail').modal('hide');
                $('#emailFallido').modal('show');
            });

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
        });
    }


    //Llamada de funciones
    cambioPeriodo();
    envioFormulario();
    
});