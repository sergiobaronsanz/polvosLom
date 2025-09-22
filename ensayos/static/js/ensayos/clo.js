document.addEventListener('DOMContentLoaded', function() {

	//Automatización columna Resultado de la tabla según valores
	var pexs= document.querySelectorAll(".pex input");
	var concentracion= document.querySelectorAll(".concentracion input");
	console.log(concentracion);

	/////Automatización columna Concentración-Peso/////
	var botonEliminar= document.getElementById("borrar-fila")
	var botonAñadir= document.getElementById("añadir-fila")




	//Función que sirve para actualizar los listerner, ya que al agregar nuevas filas no los tiene recogidos
	function listener() {
		var concentracion= document.querySelectorAll(".concentracion input");
		var pexs= document.querySelectorAll(".pex input");


		// Remueve y vuelve a agregar el mismo nodo, lo cual quita cualquier listener anterior
		concentracion.forEach(item =>{
			item.replaceWith(item.cloneNode(true));
		})

		pexs.forEach(item =>{
			item.replaceWith(item.cloneNode(true));
		})


		// Ahora se pueden agregar los listeners sin duplicarlos
		var concentracion= document.querySelectorAll(".concentracion input");
		var pexs= document.querySelectorAll(".pex input");

		
		concentracion.forEach(item => {
			item.addEventListener('change', function(){
				var id_item= item.id;
				var id_peso= id_item.replace("concentracion", "peso");
				var valor = parseFloat(item.value);
				var peso= document.getElementById(id_peso);
		
				var valorPeso= (valor/ 50).toFixed(1);
				peso.value= valorPeso;
		
			})
		});

		pexs.forEach(item => {
			item.addEventListener('change', function(){
				var id_item= item.id;
				var id_resultado= id_item.replace("pex", "resultadoPrueba");
				var valor= parseFloat(item.value);
				var resultado= document.getElementById(id_resultado);
		
				if (valor >= 0.5 ){
					resultado.value= "1";
					console.log("listo");
				} else{
					resultado.value= "2";
		
				};  
		
			});
		});
	};

	listener();
		
	botonAñadir.addEventListener('click', function(){
		listener();  
	});

	botonEliminar.addEventListener('click', function(){
		listener();  
	});



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
			const response = await fetch('/ensayos/gestorArchivos/pmax/', {
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

			//Sacamos los valores de los resultados
			let concentracion= element[2];
			let peso= (parseFloat(concentracion) / 50).toFixed(1);
			let pmax=  parseFloat(element[3].replace(",", "."));
			let dpdt= element[4];
			let oxigeno= element[7]

			
			var copiaFilaDatos = filaDatos[0].cloneNode(true); // Copia completa con contenido
			tBody.appendChild(copiaFilaDatos); // Agrega la copia al tbody
			
			
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
				if (idDato.includes("peso")) {
					input.value= peso;
				}
				if (idDato.includes("pm")) {
					input.value= pmax;
				}
				if (idDato.includes("dpdt")) {
					input.value= dpdt;
				}
				if (idDato.includes("oxigeno")) {
					input.value= oxigeno;
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

			}); 
			
			numeroResultado ++;
			var numeroEnsayos= document.getElementById("id_cloResultados-TOTAL_FORMS");
			numeroEnsayos.value= numeroResultado;
		})

		document.getElementById("fileInput").value = "";
		$('#ensayosModal').modal('hide');
		listener();
		
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
					console.log(resultado);  // Imprime cada resultado
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
