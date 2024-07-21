//General 

//Ampliación tablas
document.addEventListener('DOMContentLoaded', function() {
    var añadirFila = document.getElementById('añadir-fila');
    var tabla = document.getElementById('tabla');
    var templateRow = document.getElementById('templateRow');
    var tBody = document.getElementById('tbody');

    // Función para añadir una fila
    function addRow() {
        var newRow = templateRow.cloneNode(true);
        newRow.id = ''; // Eliminar el id para no duplicar ids
        tBody.appendChild(newRow);
    }

    // Añadir una fila al hacer clic en el botón
    añadirFila.addEventListener('click', addRow);

});