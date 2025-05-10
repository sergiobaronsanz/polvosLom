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
        let estadoPreseleccion= preseleccion.value;
		
        if (estadoPreseleccion === "1"){
            inputsTabla.forEach(input => {
                input.readOnly= false;
                
            });
            
            selectsTabla.forEach(select => {
                select.style.pointerEvents = 'auto';
				select.style.backgroundColor = '';	
            });
        }
        else {
            inputsTabla.forEach(input => {
                input.readOnly= true;
                input.value=""
            });
            console.log("Hola")
            selectsTabla.forEach(select => {
				console.log("Entró dentro")
				select.style.pointerEvents = "none";
				select.style.backgroundColor = '#eee';	
            });
        }
		pruebaTipoPolvo()
}

//Desactivamos la zona humeda si el polvo es metalico
function pruebaTipoPolvo(){
	let polvo= tipoPolvo.value;
	let estadoPreseleccion= preseleccion.value;
	
	if (estadoPreseleccion === "1" ){
		if (polvo === "1"){           
			selectsTabla.forEach(select => {
				select.style.pointerEvents = 'auto';
				select.style.backgroundColor = '';	
			});
		}
		else {
			selectsTabla.forEach(select => {
				select.style.pointerEvents = "none";
				select.style.backgroundColor = '#eee';
				select.value= "0";
			});
		}
	}
	
}

pruebaTipoPolvo();
pruebaPreseleccion();

listener();


/////Automatización columna Concentración-Peso/////
var botonEliminar= document.getElementById("borrar-fila")
var botonAñadir= document.getElementById("añadir-fila")
