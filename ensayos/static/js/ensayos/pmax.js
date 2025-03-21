
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
            var valor_serie= serie.value;
            console.log(id_serie)

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
            pm_media.value= (valor_maximo / numValores).toFixed(2);
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

        //Hacemos la media con el numero de valores que haya
        var numValores= 3;
        listaValoresMaximos.forEach(item =>{    
            if (item === 0){
                numValores= numValores -1;
            }
            dpdt_media.value= parseInt(valor_maximo / numValores);
        });
        
    };

    //Automatizacion kmax
    function kmax(){
        var dpdt= document.querySelectorAll(".dpdt input")
        //Hay que aplicar una fórmula que es...
        kmax_media.value= 44;
    };

    //Declaramos los listener
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
            item.replaceWith(item.cloneNode(true));
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
    
                var valorPeso= valor/ 50;
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
	var botonModal= document.getElementById("abrirModal");
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

	function envioArchivo(){
		const file = fileInput.files[0];
		const formData = new FormData();
		formData.append("file", file);
		formData.forEach((value, key) => {
			console.log(key, value);
		});

		fetch('/ensayos/gestorArchivos/pmax/', {
			method: "POST",
			body: formData,
			headers: {
				'X-CSRFToken': getCookie('csrftoken')
			},
		})
		.then(response => {
			return response.json();  // Convierte la respuesta en JSON
		})
		.then(data => {
			console.log("Respuesta del servidor:", data);  // Imprime toda la respuesta para revisar su formato
			if (data && data.mensaje) {
				console.log(data.mensaje);  // Si 'mensaje' existe, imprímelo
			} else {
				console.error('El mensaje no está en la respuesta');
			}
		})
		.catch(error => {
			console.log("Hubo un problema con la subida.");
			console.error("Error:", error);
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
	};

    
	//Listener para habilitar botón envio archivo en el modal
	fileInput.addEventListener('change',function(){
		habilitarEnvioModal()
	});

	//Listener para enviar archivo por POST
	botonEnviar.addEventListener('click', function(){
		envioArchivo();
	})
});
