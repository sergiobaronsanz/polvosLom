document.addEventListener('DOMContentLoaded', function() {
    // Obtener los botones de añadir y borrar fila
    var añadirFila = document.getElementById('añadir-fila');
    var borrarFila = document.getElementById('borrar-fila');
    var campoEs= this.getElementById("id_emi-resultado");
	var inductancia= document.getElementById("id_emi-inductancia");

	//Bloqueamos el campo inductancia
	inductancia.style.pointerEvents = 'none';
	inductancia.style.backgroundColor= "#e9ecef"


    function habilitarEs() {
        let resultados=document.querySelectorAll(".resultadosPruebas");
        const hayUno = Array.from(resultados).some(e => e.value === "1");
		if (hayUno) {
			campoEs.disabled = false;
		} else {
			campoEs.disabled = true;
			campoEs.value = "";
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
	habilitarEs();



	/////Envio archivo .txt en el modal///
	/////Envio archivo mediante modal/////
	var botonEnviar= document.getElementById("saveChangesBtn");
	var fileInput= document.getElementById("fileInput");
	//Empezamos con el botón desactivado y solo se activa si hay archivo
	botonEnviar.style.display= "none";

	// *En el modal* Detectamos si hay archivo o no para habilitar el botón de enviar
    function habilitarEnvioModal(){
		if (fileInput.files.length > 0) {
			botonEnviar.style.display= "flex";
		  } else {
			botonEnviar.style.display= "none";
		  }
	};

	async function envioArchivo() {
		const file = fileInput.files[0];
		const formData = new FormData();
		formData.append("file", file);
	
		try {
			const response = await fetch('/ensayos/gestorArchivos/emi/', {
				method: "POST",
				body: formData,
				headers: {
					'X-CSRFToken': getCookie('csrftoken')
				},
			});
	
			const data = await response.json();
			console.log("Respuesta del servidor:", data);
	
			if (data.resultados) {
				console.log("Datos procesados:", data.resultados);
				return data.resultados;  
			} else {
				console.error("No se encontraron resultados en la respuesta");
				return null;
			}
		} catch (error) {
			console.error("Hubo un problema con la subida:", error);
			return null;
		}
	
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
	};
		//Procesamos el archivo para que aparezcan los datos en las tablas
	function procesarArchivo(resultados){
		var filaDatos= document.querySelectorAll(".templateRow");
		var tBody= document.getElementById("tbody");
		

		//1. Borramos los registros si los hubiera
		filaDatos.forEach(element=>{
			element.remove();
		});
		

		//2. Copiamos la fila y agregamos los datos
		var numeroResultado = 0;
		resultados.forEach(element=>{
			var concentracion, energia, retardo, nEnsayo, resultado, resultadoEs
			if (element.length >= 6){
				//Sacamos los valores de los resultados
				concentracion= element[1];
				energia= element[2];
				retardo= element[3];
				nEnsayo= element[6].replace("(", "").replace(")", "");
				resultado= "";
				if (element[6] == "(10)"){
					resultado= "2";
				}else{
					resultado= "1";
				}

				
				var copiaFilaDatos = filaDatos[0].cloneNode(true); // Copia completa con contenido
				tBody.appendChild(copiaFilaDatos); // Agrega la copia al tbody
				actualizarCampos();
				habilitarEs();
				
				//Agregamos datos
				let inputs = copiaFilaDatos.querySelectorAll("input");
				let selects = copiaFilaDatos.querySelectorAll("select");
				inputs.forEach(input => {
					input.value = "";
					
					//Reemplazamos el valor al id
					let idDato= input.id;
					let nuevoId = idDato.replace(/-\d+-/, `-${numeroResultado}-`);
					input.id= nuevoId

					let nameDato= input.name;
					let nuevoName= nameDato.replace(/-\d+-/, `-${numeroResultado}-`);
					input.name= nuevoName;

					//Ingresamos los valores
					if (idDato.includes("concentracion")) {
						input.value= concentracion;
					}
					if (idDato.includes("energia")) {
						input.value= energia;
					}
					if (idDato.includes("retardo")) {
						input.value= retardo;
					}
					if (idDato.includes("numeroEnsayo")) {
						input.value= nEnsayo;
					}
				}); 

				selects.forEach(select => {
					select.value = "";
					
					//Reemplazamos el valor al id
					let idDato= select.id;
					let nuevoId = idDato.replace(/-\d+-/, `-${numeroResultado}-`);
					select.id= nuevoId
					
					let nameDato= select.name;
					let nuevoName= nameDato.replace(/-\d+-/, `-${numeroResultado}-`);
					select.name= nuevoName;

					select.value = resultado;

				}); 
				
				numeroResultado ++;
				var numeroEnsayos= document.getElementById("id_emiResultados-TOTAL_FORMS");
				numeroEnsayos.value= numeroResultado;

			}
			//Sacamos la media
			else{
				if (element[0] === 'Es (mJ):' && element.length > 1 ){
					let valores= [];
					valores.push(parseFloat(element[1].replace(',', '.')));
					valores.push(parseFloat(element[2].replace(',', '.')));
					valores.push(parseFloat(element[3].replace(',', '.')));

					filtroNan= valores.filter(n => !isNaN(n))
					let valorMinimo= Math.min(...filtroNan);
					resultadoEs = valorMinimo;

					let inputResultadoEs= document.getElementById("id_emi-resultado");

					inputResultadoEs.value=resultadoEs;

				}
			}
			
			// Eliminamos el archivo:
			document.getElementById("fileInput").value = "";
			$('#ensayosModal').modal('hide');

			
		})		
	}

    
	//Listener para habilitar botón envio archivo en el modal
	fileInput.addEventListener('change',function(){
		habilitarEnvioModal();
		
	});

	//Listener para enviar archivo por POST
	botonEnviar.addEventListener('click', async function() {
		try {
			// Espera el resultado de la función asíncrona
			const resultados = await envioArchivo();  // Usamos `await` aquí para esperar la respuesta
	
			// Verifica que `resultados` no sea null o undefined
			if (resultados) {
				resultados.forEach(resultado => {
				});
				procesarArchivo(resultados)
			} else {
				console.error('No se encontraron resultados.');
			}
		} catch (error) {
			console.error('Hubo un error al procesar los resultados:', error);
		}
	});
});
