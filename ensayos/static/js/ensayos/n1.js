console.log("hola luis");

//Variables comunes
preseleccion=document.getElementById("id_n1-pruebaPreseleccion");
tipoPolvo= document.getElementById("id_n1-tipoPolvo");
    
inputsTabla= document.querySelectorAll("#tabla input:not([name='n1Resultados-TOTAL_FORMS']):not([name='n1Resultados-INITIAL_FORMS'])");
selectsTabla= document.querySelectorAll("#tabla select");

//Activamos o desactivamos la tabla según el ensayo de preselección
function pruebaPreseleccion(){    

    preseleccion.addEventListener("change", function(){
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
    });

}

//Desactivamos la zona humeda si el polvo es metalico
function pruebaTipoPolvo(){
    console.log("ey");
    tipoPolvo.addEventListener("change", function(){
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
    });
}

pruebaPreseleccion();
pruebaTipoPolvo();
