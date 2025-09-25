

function habilitarModoCalibracion(){
	//Registramos variables
	botonCalibrado= document.getElementById('id_controlado');
	estadoCalibracion= document.getElementById('id_estadoCalibracion');
	tipoCalibracion= document.getElementById('id_tipoCalibracion');
	fechaCalibracion= document.getElementById('id_fechaCalibracion');
	fechaCaducidadCalibracion= document.getElementById('id_fechaCaducidadCalibracion');

	//Leemos el estado al refrescar
	if (botonCalibrado.checked) {
		console.log("hecho");

    } else {
		estadoCalibracion.style.pointerEvents = "none"; // evita clics
		estadoCalibracion.style.backgroundColor = "#e9ecef"; // gris para indicar bloqueado
		estadoCalibracion.style.color = "#6c757d";
		estadoCalibracion.value= "0";

		tipoCalibracion.style.pointerEvents = "none"; // evita clics
		tipoCalibracion.style.backgroundColor = "#e9ecef"; // gris para indicar bloqueado
		tipoCalibracion.style.color = "#6c757d";
		tipoCalibracion.value= "0";

		fechaCalibracion.disabled= true;
		fechaCaducidadCalibracion.disabled= true;
		console.log("no hecho");

    }

	//Leemos el estado al cambiar de estado
	botonCalibrado.addEventListener('change', function() {
    if (botonCalibrado.checked) {
        estadoCalibracion.style.pointerEvents = "auto";
		estadoCalibracion.style.backgroundColor = "";
		estadoCalibracion.style.color = "";

		tipoCalibracion.style.pointerEvents = "auto";
		tipoCalibracion.style.backgroundColor = "";
		tipoCalibracion.style.color = "";

		fechaCalibracion.disabled= false;
		fechaCaducidadCalibracion.disabled= false;

    } else {
		estadoCalibracion.style.pointerEvents = "none"; // evita clics
		estadoCalibracion.style.backgroundColor = "#e9ecef"; // gris para indicar bloqueado
		estadoCalibracion.style.color = "#6c757d";
		estadoCalibracion.value= "0";

		tipoCalibracion.style.pointerEvents = "none"; // evita clics
		tipoCalibracion.style.backgroundColor = "#e9ecef"; // gris para indicar bloqueado
		tipoCalibracion.style.color = "#6c757d";
		tipoCalibracion.value= "0";

		fechaCalibracion.disabled= true;
		fechaCalibracion.value= "";
		fechaCaducidadCalibracion.disabled= true;
		fechaCaducidadCalibracion.value= "";
    }
});





}

habilitarModoCalibracion();