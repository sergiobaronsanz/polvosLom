//FUNCIONES//

function criterioValor(){
    criterio= document.getElementById("id_criterio");
    tiempoEnsayo= document.getElementById("tiempoEnsayo");

    tiempoEnsayo.style.display= "none";

    criterio.addEventListener("change", function() {
        var criterioValor = criterio.value;
        console.log(criterioValor);
        if (criterioValor === 'manual'){
            tiempoEnsayo.style.display= "flex";
            console.log("holi");
        }
        else {
            tiempoEnsayo.style.display= "none";
            console.log("adios");
        }

    });
    
}

function calculoDesviacion(){
    //Sacamos los campos de los resultados
        // Iterar sobre los 10 campos y sumar sus valores
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

}


//LLAMADAS A FUNCIONES//

criterioValor();  

//Cada vez que se actualice algún campo se hace el cálculo
for (let i = 1; i <= 3; i++) {
    const campo = document.getElementById(`id_resultado${i}`);

    // Agregar un evento de escucha para el evento de cambio (change)
    campo.addEventListener('change', calculoDesviacion);
}
