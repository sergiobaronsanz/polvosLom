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

