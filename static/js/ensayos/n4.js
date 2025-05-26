

//Automatización pruebas N4
ensayo0= document.getElementById("ensayo0");
ensayo1= document.getElementById("ensayo1");
ensayo2= document.getElementById("ensayo2");
ensayo3= document.getElementById("ensayo3");

resultadotd= document.querySelectorAll(".resultadoTd select");


celda1= document.getElementById("id_n4Resultados-0-celda");
celda2= document.getElementById("id_n4Resultados-1-celda");
celda3= document.getElementById("id_n4Resultados-2-celda");
celda4= document.getElementById("id_n4Resultados-3-celda");

temperatura1= document.getElementById("id_n4Resultados-0-tConsigna");
temperatura2= document.getElementById("id_n4Resultados-1-tConsigna");
temperatura3= document.getElementById("id_n4Resultados-2-tConsigna");
temperatura4= document.getElementById("id_n4Resultados-3-tConsigna");

resultado1= document.getElementById("id_n4Resultados-0-resultado");
resultado2= document.getElementById("id_n4Resultados-1-resultado");
resultado3= document.getElementById("id_n4Resultados-2-resultado");
resultado4= document.getElementById("id_n4Resultados-3-resultado");

tablaNumForm= document.getElementById("id_n4Resultados-TOTAL_FORMS");



//Función para deshabilitar campos ocultos
function habilitarEnsayo(ensayo){
    let inputs= ensayo.querySelectorAll(".inputs");
    let selects= ensayo.querySelectorAll(".selects");
    
    ensayo.style.display="";

    inputs.forEach((input) =>{
        input.disabled= false;
    });

    selects.forEach((select) =>{
        select.disabled= false;
    });


}

function deshabilitarEnsayo(ensayo){
    var inputs= ensayo.querySelectorAll(".inputs");
    var selects= ensayo.querySelectorAll(".selects");

    console.log(inputs)

    ensayo.style.display="none";
    inputs.forEach((input) =>{
        input.disabled= true;
        console.log("deshabilitado");
    });

    selects.forEach((select) =>{
        select.disabled= true;
    });
}

const urlCompleta = window.location.href;
//Iniciamos, todas oculas menos ensayo 1 que tiene que ir definida en 140ºC con celda de 100mm

if (urlCompleta.includes("nueva")) {
    
    deshabilitarEnsayo(ensayo1);
    deshabilitarEnsayo(ensayo2);
    deshabilitarEnsayo(ensayo3);

    tablaNumForm.value= 1;

    celda1.value= "2";
    temperatura1.value= "3";
} else {
    resultadotd.forEach(resultado => {
		//Si algún ensayo no tiene valor en el select eso es que no tiene que aparecer, se le quita y se le anula el required
		var numeroBucles= 0
        if (resultado.value === "0"){
			numeroBucles ++;
            const numero = resultado.id.match(/-(\d+)-/);
            const numeroValor= numero[1];
            const idEnsayo= "ensayo" + numeroValor;
            console.log("el valor del ensayo es:" + idEnsayo);
            
            const ensayoseleccionado= document.getElementById(idEnsayo);
            ensayoseleccionado.style.display="none";

			let inputs= ensayoseleccionado.querySelectorAll(".inputs");
			let selects= ensayoseleccionado.querySelectorAll(".selects");

			inputs.forEach((input) =>{
				input.disabled= true;
			});

			selects.forEach((select) =>{
				select.disabled= true;
			});


            
        }
		//Actualizamos el número de filas de la tabla
		let numeroFilastotales= tablaNumForm.value
		tablaNumForm.value= numeroFilastotales-numeroBucles
		
    });
}


//Caso 1
resultado1.addEventListener("change", r =>{
    console.log("hola");
    if (resultado1.value === "1"){
        habilitarEnsayo(ensayo1)
        tablaNumForm.value= 2;
    
        celda2.value= "1";
        temperatura2.value= "3";
    }else{
        deshabilitarEnsayo(ensayo1);
        deshabilitarEnsayo(ensayo2);
        deshabilitarEnsayo(ensayo3);
        tablaNumForm.value= 1;

        
        resultado2.value="0";
        celda2.value= "0";
    }
});

//Caso2
resultado2.addEventListener("change", r =>{
    console.log("hola");
    if (resultado2.value === "2"){
        habilitarEnsayo(ensayo2)
        tablaNumForm.value= 3;

    
        celda3.value= "2";
        temperatura3.value= "2";
    }else{
        deshabilitarEnsayo(ensayo2);
        deshabilitarEnsayo(ensayo3);
        tablaNumForm.value= 2;


        resultado3.value="0";
        celda3.value= "0";
    }

});

//Caso3
resultado3.addEventListener("change", r =>{
    console.log("hola");
    if (resultado3.value === "1"){
        habilitarEnsayo(ensayo3);
        tablaNumForm.value= 4;

        celda4.value= "2";
        temperatura4.value= "1";

    }else{
        deshabilitarEnsayo(ensayo3);
        tablaNumForm.value= 3;

        celda4.value= "0";

        if(resultado3.value!="2"){
            resultado3.value="0";
        }
        
    }
    
});

