console.log("hola luis");

var preseleccion=document.getElementById("id_n1-pruebaPreseleccion");
var tipoPolvo= document.getElementById("id_n1-tipoPolvo");
    
let inputsTabla= document.querySelectorAll("#tabla input:not([name='n1Resultados-TOTAL_FORMS']):not([name='n1Resultados-INITIAL_FORMS'])");
let selectsTabla= document.querySelectorAll("#tabla select");

function listener(){

	preseleccion.addEventListener("change", function(){
		pruebaPreseleccion();
	});

	tipoPolvo.addEventListener("change", function(){
		pruebaTipoPolvo();

	});
}

//Activamos o desactivamos la tabla según el ensayo de preselección
function pruebaPreseleccion(){   
        estadoPreseleccion= preseleccion.value;
        if (estadoPreseleccion === "1"){
            inputsTabla.forEach(input => {
                input.readOnly= false;
                
            });
            
            selectsTabla.forEach(select => {
                select.disabled= false;
            });
        }
        else {
            inputsTabla.forEach(input => {
                input.readOnly= true;
                input.value=""
            });
            
            selectsTabla.forEach(select => {
                select.disabled= true;
                select.value= "0";
            });
        }
}

//Desactivamos la zona humeda si el polvo es metalico
function pruebaTipoPolvo(){
	polvo= tipoPolvo.value;
	if (polvo === "1"){           
		selectsTabla.forEach(select => {
			select.disabled= false;
		});
	}
	else {
		selectsTabla.forEach(select => {
			select.disabled= true;
			select.value= "0";
		});
	}
}


pruebaPreseleccion();
pruebaTipoPolvo();
listener();


/////Automatización columna Concentración-Peso/////
var botonEliminar= document.getElementById("borrar-fila")
var botonAñadir= document.getElementById("añadir-fila")
