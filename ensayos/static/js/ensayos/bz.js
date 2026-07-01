document.addEventListener('DOMContentLoaded', function() {

    //SELECTOR CAMBIO FUENTE IGNICIÓN-TIEMPO
    const selectorFuente = document.getElementById("id_bz-tipoFuenteIgnicion");
    const selectorTiempo = document.getElementById("id_bz-tiempoFuenteIgnicion");

    function actualizarTiempo() {
        selectorTiempo.value = selectorFuente.value === "1" ? 5 : 2;
    }

    actualizarTiempo();
    selectorFuente.addEventListener("change", actualizarTiempo);

    
    //AUTOMATIZACIÓN CAMBIO RESULTADOS SEGÚN TIPO IGNICION
    const selectorCombustion = document.querySelectorAll(".tipoIgnicion select");
    const selectorResultado = document.querySelectorAll(".resultado input");

	/////Automatización columna Concentración-Peso/////
	var botonEliminar= document.getElementById("borrar-fila")
	var botonAñadir= document.getElementById("añadir-fila")


	//Función que sirve para actualizar los listerner, ya que al agregar nuevas filas no los tiene recogidos
	function listener() {
        var selectorCombustion = document.querySelectorAll(".tipoIgnicion select");
        var selectorResultado = document.querySelectorAll(".resultado input");
	
		// Remueve y vuelve a agregar el mismo nodo, lo cual quita cualquier listener anterior
		/*selectorCombustion.forEach(item =>{
			item.replaceWith(item.cloneNode(true));
		})

		selectorResultado.forEach(item =>{
			item.replaceWith(item.cloneNode(true));
		})*/


		// Ahora se pueden agregar los listeners sin duplicarlos
		var selectorCombustion= document.querySelectorAll(".tipoIgnicion select");
		var selectorResultado= document.querySelectorAll(".resultado input");

		
		selectorCombustion.forEach(item => {
			item.addEventListener('change', function(){
				var id_item= item.id;
                var selectorCombustion= document.getElementById(id_item);
				var id_resultado= id_item.replace("tipoIgnicion", "resultado");
				var selectorResultado= document.getElementById(id_resultado);
                
				selectorResultado.value = selectorCombustion.value;
		
			})
		});
	};

	listener();
		
	botonAñadir.addEventListener('click', function(){
		listener();  
	});

	botonEliminar.addEventListener('click', function(){
		listener();  
	});


});