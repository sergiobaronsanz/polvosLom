//Fijar proporciones

function fijarProporcion(){
    let proporcion1= document.getElementById("id_o1Resultados-0-proporcion");
    let proporcion2= document.getElementById("id_o1Resultados-1-proporcion");
    let proporcion3= document.getElementById("id_o1Resultados-2-proporcion");
    let proporcion4= document.getElementById("id_o1Resultados-3-proporcion");
    let proporcion5= document.getElementById("id_o1Resultados-4-proporcion");

    proporcion1.value="1";
    proporcion2.value="2";
    proporcion3.value="3";
    proporcion4.value="4";
    proporcion5.value="5";
}

function calcularResultados(){
    let tiempos= document.querySelectorAll(".tiempo");
    let resultado1= document.getElementById("id_o1Resultados-0-resultado");
    let resultado2= document.getElementById("id_o1Resultados-1-resultado");
    let resultado3= document.getElementById("id_o1Resultados-2-resultado");
    let resultado4= document.getElementById("id_o1Resultados-3-resultado");
    let resultado5= document.getElementById("id_o1Resultados-4-resultado");

    let tiempos1 = [];
    let tiempos2 = [];
    let tiempos3 = [];
    let tiempos4 = [];
    let tiempos5 = [];


    //Separamos los tiempos en cada fila
    tiempos.forEach(tiempo => {
        let idTiempo= tiempo.id;
        let regex = /id_o1Resultados-(\d+)-tiempo(\d+)/;

        // Aplicamos la RegEx para capturar los valores de X e Y
        let matches = idTiempo.match(regex);
        let valorX="";

        if (matches) {
            valorX = matches[1]; // Captura el valor de X
        }
        console.log(valorX)

        //fila1
        if (valorX === "0"){
            tiempos1.push(tiempo)
        }
        //fila2
        if (valorX === "1"){
            tiempos2.push(tiempo)
        }
        //fila3
        if (valorX === "2"){
            tiempos3.push(tiempo)
        }
        //fila4
        if (valorX === "3"){
            tiempos4.push(tiempo)
        }    
        //fila5
        if (valorX === "4"){
            tiempos5.push(tiempo)
        }        
              
                
    });

    //Calculamos el resultado de cada fila
    function resultadoFila(tiempos, resultado){
        tiempos.forEach(tiempo =>{
            tiempo.addEventListener("change", event=>{
                let sumaTotal= 0;
                let numTotal=0;
                tiempos.forEach(tiempoc => {
				if (tiempoc.value && !isNaN(tiempoc.value)) {
					// Convertir a número, redondear al entero más cercano y asegurar entero
					const valorRedondeado = Math.round(parseFloat(tiempoc.value));
					
					sumaTotal += valorRedondeado;
					numTotal += 1;
				}
});
                nuevoResultado= sumaTotal/numTotal;
                resultado.value= parseFloat(nuevoResultado).toFixed(1);
            })
        })

    }

    resultadoFila(tiempos1, resultado1);
    resultadoFila(tiempos2, resultado2);
    resultadoFila(tiempos3, resultado3);
    resultadoFila(tiempos4, resultado4);
    resultadoFila(tiempos5, resultado5);

    
}

    
    

//Funciones
fijarProporcion();
calcularResultados();