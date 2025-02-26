

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

const urlCompleta = window.location.href;
//Iniciamos, todas oculas menos ensayo 1 que tiene que ir definida en 140ºC con celda de 100mm

if (urlCompleta.includes("nueva")) {
    console.log("holaaaaiu");
    if (celda2===null){
        ensayo1.style.display="none";
        tablaNumForm.value=2
    }
    if (celda3===null){
        ensayo2.style.display="none";
        tablaNumForm.value=3
    }
    if (celda4===null){
        ensayo3.style.display="none";
        tablaNumForm.value=4
    }

    celda1.value= "2";
    temperatura1.value= "3";
} else {
    resultadotd.forEach(resultado => {
        if (resultado.value === "0"){
            const numero = resultado.id.match(/-(\d+)-/);
            const numeroValor= numero[1];
            const idEnsayo= "ensayo" + numeroValor;
            console.log(idEnsayo);
            
            const ensayoseleccionado= document.getElementById(idEnsayo);
            ensayoseleccionado.style.display="none";
            
        }
    });
}


//Caso 1
resultado1.addEventListener("change", r =>{
    console.log("hola");
    if (resultado1.value === "1"){
        ensayo1.style.display="";
        tablaNumForm.value= 2;
    
        celda2.value= "1";
        temperatura2.value= "3";
    }else{
        ensayo1.style.display="none";
        ensayo2.style.display="none";
        ensayo3.style.display="none";
        tablaNumForm.value= 1;

        
        resultado2.value="0";
    }
});

//Caso2
resultado2.addEventListener("change", r =>{
    console.log("hola");
    if (resultado2.value === "2"){
        ensayo2.style.display="";
        tablaNumForm.value= 3;

    
        celda3.value= "2";
        temperatura3.value= "2";
    }else{
        ensayo2.style.display="none";
        ensayo3.style.display="none";
        tablaNumForm.value= 2;


        resultado3.value="0";
    }

});

//Caso3
resultado3.addEventListener("change", r =>{
    console.log("hola");
    if (resultado3.value === "1"){
        ensayo3.style.display="";
        tablaNumForm.value= 4;

        celda4.value= "2";
        temperatura4.value= "1";

    }else{
        ensayo3.style.display="none";
        tablaNumForm.value= 3;

        if(resultado3.value!="2"){
            resultado3.value="0";
        }

        
        
    }
    
});

