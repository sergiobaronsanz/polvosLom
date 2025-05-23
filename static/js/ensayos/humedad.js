//FUNCIONES//

function criterioValor(){
    criterio= document.getElementById("id_criterio");
    tiempoEnsayo= document.getElementById("id_tiempoEnsayo");
    inputTiempoEnsayo= document.getElementById("id_tiempoEnsayo");

    tiempoEnsayo.disabled= true;
    tiempoEnsayo.value= "";

    criterio.addEventListener("change", function() {
        var criterioValor = criterio.value;
        console.log(criterioValor);
        if (criterioValor === 'manual'){
            tiempoEnsayo.disabled= false;
            console.log("holi");
        }
        else {
            tiempoEnsayo.disabled= false;
            inputTiempoEnsayo.value= "";
            console.log("adios");
        }

    });
    
}

function calculoDesviacion(){
    //Ocultamos los 7 campos
    camposOcultos= document.getElementsByClassName("campoOculto");

    for (let i=0; i < camposOcultos.length; i++){
        camposOcultos[i].style.display="none";
        var input = camposOcultos[i].querySelector('input');
        input.removeAttribute("required");
    }

    function calculo(){
        let suma= 0;
        let valores=[];
        for (let i = 1; i <= 3; i++) {
            const valorCampo = parseFloat(document.getElementById(`id_resultado${i}`).value.replace(",","."));
            if (!isNaN(valorCampo)){
                valores.push(valorCampo);
                suma+= valorCampo;
                console.log(valores);
                
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
                camposOcultos[i].style.flexDirection = "column";
                var input = camposOcultos[i].querySelector('input');
                input.setAttribute("required", "required");
            }
        }else{
            for (let i=0; i < camposOcultos.length; i++){
                camposOcultos[i].style.display="none";
                var input = camposOcultos[i].querySelector('input');
                input.removeAttribute("required");
            }
        }
    }
        
    for (let i = 1; i <= 3; i++) {
        const campo = document.getElementById(`id_resultado${i}`);
    
        // Agregar un evento de escucha para el evento de cambio (change)
        campo.addEventListener('change', calculo);
    }
}

function resultadoNoDeterminado(){
    var botonND= document.getElementById("boton-nd");
    var desviacion= document.getElementById("id_desviacion");
    var resultado1= document.getElementById("id_resultado1");
    var resultado2= document.getElementById("id_resultado2");
    var resultado3= document.getElementById("id_resultado3");

    botonND.addEventListener("click", function(){
        desviacion.value= 0;
        resultado1.value= "N/D";
        resultado2.value= "N/D";
        resultado3.value= "N/D";
    });

}
//LLAMADAS A FUNCIONES//

criterioValor();  

//Cada vez que se actualice algún campo se hace el cálculo
calculoDesviacion();

resultadoNoDeterminado();