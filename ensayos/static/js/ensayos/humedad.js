//FUNCIONES//

function criterioValor(){
    criterio= document.getElementById("id_criterio");
    tiempoEnsayo= document.getElementById("tiempoEnsayo");

    tiempoEnsayo.style.opacity= "0";
    tiempoEnsayo.value= "";

    criterio.addEventListener("change", function() {
        var criterioValor = criterio.value;
        console.log(criterioValor);
        if (criterioValor === 'manual'){
            tiempoEnsayo.style.opacity= "1";
            console.log("holi");
        }
        else {
            tiempoEnsayo.style.opacity= "0";
            tiempoEnsayo.value= "";
            console.log("adios");
        }

    });
    
}

function calculoDesviacion(){
    //Ocultamos los 7 campos
    camposOcultos= document.getElementsByClassName("campoOculto");

    for (let i=0; i < camposOcultos.length; i++){
        camposOcultos[i].style.display="none";
    }

    function calculo(){
        let suma= 0;
        let valores=[];
        for (let i = 1; i <= 3; i++) {
            const valorCampo = parseFloat(document.getElementById(`id_resultado${i}`).value);
            if (!isNaN(valorCampo)){
                valores.push(valorCampo);
                suma+= valorCampo;
            }
        }

        //Calculamos la desviacion típica
        let media= suma/valores.length;
        let sumatorioCuadrados= valores.reduce((acumulador, valor) => acumulador + Math.pow(valor - media, 2), 0);
        const desviacionEstandar = Math.sqrt(sumatorioCuadrados / (valores.length - 1));
        
        //Ponemos el valor en el campo desviacion
        const desviacion= document.getElementById("id_desviacion");
        desviacion.value= desviacionEstandar.toFixed(2);

        //Mostramos o ocultamos los campos dependiendo de la desviación
        if (desviacionEstandar>= 0.15){
            for (let i=0; i < camposOcultos.length; i++){
                camposOcultos[i].style.display="flex";
            }
        }else{
            for (let i=0; i < camposOcultos.length; i++){
                camposOcultos[i].style.display="none";
            }
        }
    }
        
    for (let i = 1; i <= 3; i++) {
        const campo = document.getElementById(`id_resultado${i}`);
    
        // Agregar un evento de escucha para el evento de cambio (change)
        campo.addEventListener('change', calculo);
    }
}


//LLAMADAS A FUNCIONES//

criterioValor();  

//Cada vez que se actualice algún campo se hace el cálculo
calculoDesviacion();
