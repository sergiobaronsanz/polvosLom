//Automatización columna Resultado de la tabla según valores
pexs= document.querySelectorAll(".pex input");
concentracion= document.querySelectorAll(".concentracion input");
console.log(concentracion);


pexs.forEach(item => {
    item.addEventListener('change', function(){
        var id_item= item.id;
        var id_resultado= id_item.replace("pex", "resultadoPrueba");
        var valor= parseFloat(item.value);
        var resultado= document.getElementById(id_resultado);

        if (valor >= 0.5 ){
            resultado.value= "1";
            console.log("listo");
        } else{
            resultado.value= "2";

        };  

    });
});

//Automatización columna Concentración-Peso
concentracion.forEach(item => {
    item.addEventListener('change', function(){
        var id_item= item.id;
        var id_peso= id_item.replace("concentracion", "peso");
        var valor = parseFloat(item.value);
        var peso= document.getElementById(id_peso);

        var valorPeso= valor/ 50;
        peso.value= valorPeso;

        console.log(valorPeso);
    })
});




