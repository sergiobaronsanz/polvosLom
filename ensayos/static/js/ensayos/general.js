//General 

//Ampliación tablas
document.addEventListener('DOMContentLoaded', function() {
    var añadirFila = document.getElementById('añadir-fila');
    var borrarFila = document.getElementById('borrar-fila');
    var tabla = document.getElementById('tabla');
    var templateRow = document.querySelectorAll(".templateRow")
    var formulario= document.getElementById("id_"+ ensayo + "Resultados-TOTAL_FORMS")
    // última template row
    var lastTemplateRow= templateRow[templateRow.length -1];
    var tBody = document.getElementById('tbody');

    // Función para añadir una fila
    function addRow() {
        console.log("hola");
        var newRow = lastTemplateRow.cloneNode(true);

        //Los dejamos vacíos
        var inputs = newRow.querySelectorAll('input');
        inputs.forEach(function(input) {
            input.value = '';
        });

        // Obtener el nombre del campo del input en la fila clonada
        var inputs = newRow.querySelectorAll('input');
        var select= newRow.querySelectorAll('select');
        if (inputs.length > 0 & select.length > 0 ) {
            //Sacamos el número 
            var entradasFormulario= parseInt(formulario.value);
            var siguienteNumero= entradasFormulario;
            
            select.forEach(function(select){
                // Obtén el atributo name del input
                var name = select.getAttribute('name');
        
                // Sustituye el número en el atributo name con el nuevo número
                var nuevoName = name.replace(/\d+/, siguienteNumero);
        
                // Establece el nuevo name en el input
                select.setAttribute('name', nuevoName);
        
                // Opcional: Imprimir para verificar
                console.log('Nombre antiguo: ' + name + ', Nombre nuevo: ' + nuevoName);
            });

            inputs.forEach(function(input) {
                // Obtén el atributo name del input
                var name = input.getAttribute('name');
        
                // Sustituye el número en el atributo name con el nuevo número
                var nuevoName = name.replace(/\d+/, siguienteNumero);
        
                // Establece el nuevo name en el input
                input.setAttribute('name', nuevoName);
        
                // Opcional: Imprimir para verificar
                console.log('Nombre antiguo: ' + name + ', Nombre nuevo: ' + nuevoName);
            });

            //Le decimos al formulario que va a ser uno más
            formulario.value= entradasFormulario + 1;
            console.log(formulario.value);

        } else {
            console.log("No se encontraron inputs en la fila clonada.");
        }
        newRow.id = ''; // Eliminar el id para no duplicar ids
        tBody.appendChild(newRow);
    }

    function deleteRow(){
        if (lastTemplateRow) {
            //Borramos la última fila del form y reseteamos el numero de inputs del form
            lastTemplateRow.parentNode.removeChild(lastTemplateRow);
            formulario.value= parseInt (formulario.value) - 1;

        }
        //Actualizamos el ultimo template
        templateRow = document.querySelectorAll(".templateRow")
        lastTemplateRow= templateRow[templateRow.length -1];


    }
    // Añadir una fila al hacer clic en el botón
    añadirFila.addEventListener('click', addRow);
    borrarFila.addEventListener('click', deleteRow);

});