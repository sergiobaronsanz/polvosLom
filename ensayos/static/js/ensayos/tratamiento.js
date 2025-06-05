//Control habilitar deshabilitar campos

secado= document.getElementById("secado");
molido= document.getElementById("molido");
tamizado= document.getElementById("tamizado");

grupoSecado= document.querySelectorAll(".secado");
grupoMolido= document.querySelectorAll(".molido");
grupoTamizado= document.querySelectorAll(".tamizado");


//Función para mostar o ocultar campos
function mostrarCampos(grupo){
	console.log("hola");
	grupo.forEach(element => {
		element.disabled= false;
		element.required= true;
	});
}

function ocultarCampos(grupo){
	console.log("adios");
	grupo.forEach(element => {
		element.disabled= true;
		element.required= false;
		element.value= "";
	});
}



//Iniciamos todos ocultos

if (secado.value == "1"){
	ocultarCampos(grupoSecado);
}
else{
	mostrarCampos(grupoSecado);
}

if (molido.value == "1"){
	ocultarCampos(grupoMolido);
}
else{
	mostrarCampos(grupoMolido);
}

if (tamizado.value == "1"){
	ocultarCampos(grupoTamizado);
}
else{
	mostrarCampos(grupoTamizado);
}


//Control de los cambios de variable
secado.addEventListener("change", function () {
	if (secado.value == "1"){
		ocultarCampos(grupoSecado);
	}
	else{
		mostrarCampos(grupoSecado);
	}
});

molido.addEventListener("change", function () {
	if (molido.value == "1"){
		ocultarCampos(grupoMolido);
	}
	else{
		mostrarCampos(grupoMolido);
	}
});

tamizado.addEventListener("change", function () {
	if (tamizado.value == "1"){
		ocultarCampos(grupoTamizado);
	}
	else{
		mostrarCampos(grupoTamizado);
	}
});



//Cambio lista tamices
campoEquipo= document.getElementById("id_tratamiento-equipoTamizado")

//Envío data post
async function cambioLista(equipo) {
	const formData = new FormData();
	formData.append("equipo", equipo)

	try {
		const response = await fetch('/ensayos/listaTamices/', {
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

campoEquipo.addEventListener("change", async function(){
	let equipo= campoEquipo.value
	let tamices = document.getElementById("id_tratamiento-tamiz")
	
	//Limpiamos la lista de tamices
	tamices.innerHTML = "";
	const primeraOpcion= document.createElement("option")
	primeraOpcion.value= 0;
	primeraOpcion.textContent= "-"
	tamices.appendChild(primeraOpcion)

	console.log(equipo);

	const resultados = await cambioLista(equipo);

	resultados.forEach(resultado => {
		const option = document.createElement("option");
		option.value = resultado.id;
		option.textContent = resultado.nombre;
		tamices.appendChild(option);
	});
})