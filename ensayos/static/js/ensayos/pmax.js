
document.addEventListener('DOMContentLoaded', function() {
    /////Automatización columna Concentración-Peso/////
    var botonEliminar= document.getElementById("borrar-fila")
    var botonAñadir= document.getElementById("añadir-fila")
        
        /////Cálculo de Presión media, dp/dt media y kmax/////
    var pm_media= document.getElementById("id_pmax-pm_media");
    var dpdt_media= document.getElementById("id_pmax-dpdt_media");
    var kmax_media= document.getElementById("id_pmax-kmax");

    //Automatizamos las presiones
    function presionMedia(){
        var pms= document.querySelectorAll(".pm input")


        //Sacamos las variables necesarias
        var sumaPresiones= 0;
        var numPresiones= 0;
        var listaValoresMaximos= [0,0,0];
        var listaValores1= [];
        var listaValores2= [];
        var listaValores3= [];
        var valor_maximo= 0.0;

        //Sacamos los valores máximos de cada serie
        pms.forEach(item =>{
            var id_item= item.id;
            var id_serie= id_item.replace("pm_serie", "serie");
			var serie= document.getElementById(id_serie);
            var serie= document.getElementById(id_serie);
            var valor_serie= serie.value;
            

            if(valor_serie=== "1"){
                
                if(item.value){
                    listaValores1.push(item.value);
                }
                
            }

            if(valor_serie=== "2"){
                
                if(item.value){
                    listaValores2.push(item.value);
                }
                
            }

            if(valor_serie=== "3"){
                
                if(item.value){
                    listaValores3.push(item.value);
                }
                
            }          
        })

        if (listaValores1.length > 0){
            listaValoresMaximos[0]= Math.max(...listaValores1);
        }

        if (listaValores2.length > 0){
            listaValoresMaximos[1]= Math.max(...listaValores2);
        }

        if (listaValores3.length > 0){
            listaValoresMaximos[2]= Math.max(...listaValores3);
        }


        valor_maximo= listaValoresMaximos[0] + listaValoresMaximos[1] + listaValoresMaximos[2];

        //Hacemos la media con el numero de valores que haya
        var numValores= 3;
        listaValoresMaximos.forEach(item =>{    
            if (item === 0){
                numValores= numValores -1;
            }
			let resultado=0;
			
			if (valor_maximo){
				resultado= (Math.round(valor_maximo / numValores * 10) / 10).toFixed(1);
			}
			
			pm_media.value = resultado;
			
        });
        
    };

    //Automatizamos las dPdT
    function dpdtMedia(){
        var dpdt= document.querySelectorAll(".dpdt input")

        //Sacamos las variables necesarias
        var sumaPresiones= 0;
        var numPresiones= 0;
        var listaValoresMaximos= [0,0,0];
        var listaValores1= [];
        var listaValores2= [];
        var listaValores3= [];
        var valor_maximo= 0.0;

        //Sacamos los valores máximos de cada serie
        dpdt.forEach(item =>{
            var id_item= item.id;
            var id_serie= id_item.replace("dpdt_serie", "serie");
            var serie= document.getElementById(id_serie);
            var valor_serie= serie.value;

            if(valor_serie=== "1"){
                
                if(item.value){
                    listaValores1.push(item.value);
                }
                
            }

            if(valor_serie=== "2"){
                
                if(item.value){
                    listaValores2.push(item.value);
                }
                
            }

            if(valor_serie=== "3"){
                
                if(item.value){
                    listaValores3.push(item.value);
                }
                
            }          
        })

        if (listaValores1.length > 0){
            listaValoresMaximos[0]= Math.max(...listaValores1);
        }

        if (listaValores2.length > 0){
            listaValoresMaximos[1]= Math.max(...listaValores2);
        }

        if (listaValores3.length > 0){
            listaValoresMaximos[2]= Math.max(...listaValores3);
        }

        valor_maximo= listaValoresMaximos[0] + listaValoresMaximos[1] + listaValoresMaximos[2];
		console.log("el valor dpdt max es:" + valor_maximo/3)

        //Hacemos la media con el numero de valores que haya
        var numValores= 3;
        listaValoresMaximos.forEach(item =>{    
            if (item === 0){
                numValores= numValores -1;
            }
			let resultado= 0
			if (valor_maximo){
				resultado= (Math.round(valor_maximo / numValores).toFixed(0));
			}
            dpdt_media.value= resultado;
        });
        
    };

    //Automatizacion kmax
    function kmax(){
        var dpdt= document.querySelectorAll(".dpdt input")
        //Hay que aplicar una fórmula que es...
		valorVelocidad= dpdt_media.value;
		let raizCubica = Math.cbrt(20/1000);
		let resultado= Math.round(valorVelocidad * raizCubica)
		console.log("la raiz es: " + raizCubica + "el resultado es: " + (valorVelocidad * raizCubica))
        kmax_media.value= resultado
    };

    //Declaramos los listener para que se puedan actualizar cuando se borren id
    function listener() {
        var concentracion= document.querySelectorAll(".concentracion input");
        var pms = document.querySelectorAll(".pm input");
        var dpdt = document.querySelectorAll(".dpdt input");
        var series = document.querySelectorAll(".serie select");
    
        // Remueve y vuelve a agregar el mismo nodo, lo cual quita cualquier listener anterior
        concentracion.forEach(item =>{
            item.replaceWith(item.cloneNode(true));
        })

        pms.forEach(item => {
            item.replaceWith(item.cloneNode(true));
        });
    
        dpdt.forEach(item => {
            item.replaceWith(item.cloneNode(true));
        });
    
        series.forEach(item => {
			let valorAnteriorItem= item.value;
			console.log("el valor de la serie es<" + valorAnteriorItem)
            let nuevoItem = item.cloneNode(true); // Clonar el nodo
    		nuevoItem.value = valorAnteriorItem;  // Restaurar el valor antes de reemplazarlo

			item.replaceWith(nuevoItem)
		});
    
        // Ahora se pueden agregar los listeners sin duplicarlos
        concentracion= document.querySelectorAll(".concentracion input");
        pms = document.querySelectorAll(".pm input");
        dpdt = document.querySelectorAll(".dpdt input");
        series = document.querySelectorAll(".serie select");

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
    
        pms.forEach(item => {
            item.addEventListener('change', function() {
                presionMedia();
            });
        });
    
        dpdt.forEach(item => {
            item.addEventListener('change', function() {
                dpdtMedia();
                kmax();
            });
        });
    
        series.forEach(item => {
            item.addEventListener('change', function() {
                presionMedia();
                dpdtMedia();
                kmax();
            });
        });
    }
    listener();
    
    botonAñadir.addEventListener('click', function(){
        listener();  
    });

    botonEliminar.addEventListener('click', function(){
        listener();  
    });




	/////Envio archivo .txt en el modal///
	/////Envio archivo mediante modal/////
	var botonEnviar= document.getElementById("saveChangesBtn");
	var fileInput= document.getElementById("fileInput");
	//Empezamos con el botón desactivado y solo se activa si hay archivo
	botonEnviar.style.display= "none";

	// *En el modal* Detectamos si hay archivo o no para habilitar el botón de enviar
    function habilitarEnvioModal(){
		console.log("hola");
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
			let serie= element[1];
			let pmax=  parseFloat(element[3].replace(",", "."));
			let dpdt= element[4];

			
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
				if (idDato.includes("pm_serie")) {
					input.value= pmax;
				}
				if (idDato.includes("dpdt_serie")) {
					input.value= dpdt;
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

				console.log("la serie es" + serie)
				select.value = serie;
				console.log("El valor es" + select.value)
				console.log(select.id)
				console.log("Nuevo valor del select:", select.value); // Muestra el nuevo valor
			}); 
			
			numeroResultado ++;
			var numeroEnsayos= document.getElementById("id_pmaxResultados-TOTAL_FORMS");
			numeroEnsayos.value= numeroResultado;
		})

		//Recalculamos las medias
		listener();
		presionMedia();
		dpdtMedia();
		kmax();

		document.getElementById("fileInput").value = "";
		$('#ensayosModal').modal('hide');
		
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
