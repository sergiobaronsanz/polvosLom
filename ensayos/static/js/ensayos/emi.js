document.addEventListener('DOMContentLoaded', function() {
    // Obtener los botones de añadir y borrar fila
    var añadirFila = document.getElementById('añadir-fila');
    var borrarFila = document.getElementById('borrar-fila');
    var campoEs= this.getElementById("id_emi-resultado");

    function habilitarEs() {
        console.log("dentroooo");
        let resultados=document.querySelectorAll(".resultadosPruebas");
        for (let e of resultados) {
            console.log(e.value);
            if (e.value === "1") {
                campoEs.disabled = false;
                break; // Sale del bucle cuando encuentra el primer "1"
            }
            campoEs.disabled = true;
            campoEs.value= "";
        }
    }

    // Función para actualizar los campos y asegurarse de que solo se agregue el evento una vez
    function actualizarCampos() {
        let resultados = document.querySelectorAll(".resultadosPruebas");
        console.log("Actualizando campos...", resultados);

        resultados.forEach(e => {
            // Remover cualquier evento previo para evitar duplicaciones
            e.removeEventListener("change", habilitarEs);
            // Agregar el evento solo una vez
            e.addEventListener("change", habilitarEs);
        });
    }

    // Añadir eventos a los botones
    añadirFila.addEventListener("click", actualizarCampos);
    borrarFila.addEventListener("click", actualizarCampos);

    // Llamar la función al inicio para configurar los eventos en los elementos existentes
    actualizarCampos();

});