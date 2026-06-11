document.addEventListener("DOMContentLoaded", () => {
    console.log("inicio bien");

    // Campo año
    const year = document.getElementById("id_fechaYear");

    // Loader
    const loader = document.getElementById("loader");

    // Envío de formulario
    function envioFormulario() {
        const botonEnvio = document.getElementById("generarReporte");

        botonEnvio.addEventListener("click", function () {

            // Mostrar loader
            loader.style.display = "flex";
            botonEnvio.disabled = true;

            const datos = {
                fechaYear: year.value
            };

            console.log(datos);

            fetch('/reporte/', {
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

                if (contentType && contentType.includes('application/pdf')) {

                    return response.blob().then(blob => {

                        const url = window.URL.createObjectURL(blob);

                        const contentDisposition = response.headers.get('Content-Disposition');

                        const filename = contentDisposition
                            ? contentDisposition.split('filename=')[1].replace(/"/g, '')
                            : 'archivo.pdf';

                        const a = document.createElement('a');
                        a.href = url;
                        a.download = filename;

                        document.body.appendChild(a);
                        a.click();
                        a.remove();

                        window.URL.revokeObjectURL(url);

                        console.log('Archivo descargado correctamente');

                        // Cerrar modal de selección si existe
                        $('#seleccionReporte').modal('hide');

                        return { mensaje: "Reporte generado" };
                    });

                } else {
                    return response.json();
                }
            })
            .then(data => {

                console.log("Respuesta:", data);

                if (data && data.mensaje === "Reporte generado") {
                    console.log("Reporte generado correctamente");
                }
            })
            .catch(error => {

                console.error('Error en la solicitud:', error);

                $('#seleccionReporte').modal('hide');
                $('#emailFallido').modal('show');
            })
            .finally(() => {

                // Ocultar loader siempre
                loader.style.display = "none";
                botonEnvio.disabled = false;
            });
        });
    }

    function getCookie(name) {
        let cookieValue = null;

        if (document.cookie && document.cookie !== '') {

            const cookies = document.cookie.split(';');

            for (let i = 0; i < cookies.length; i++) {

                const cookie = cookies[i].trim();

                if (cookie.substring(0, name.length + 1) === (name + '=')) {

                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );

                    break;
                }
            }
        }

        return cookieValue;
    }

    envioFormulario();
});