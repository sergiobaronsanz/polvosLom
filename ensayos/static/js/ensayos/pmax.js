document.addEventListener('DOMContentLoaded', function() {
    /////Automatización columna Concentración-Peso/////
    console.log("hola");
    var botonEliminar= document.getElementById("borrar-fila")
    var botonAñadir= document.getElementById("añadir-fila")
    concentracion= document.querySelectorAll(".concentracion input");

    concentracion.forEach(item => {
        item.addEventListener('change', function(){
            var id_item= item.id;
            var id_peso= id_item.replace("concentracion", "peso");
            var valor = parseFloat(item.value);
            var peso= document.getElementById(id_peso);

            var valorPeso= valor/ 50;
            peso.value= valorPeso;
        })
    });

        /////Cálculo de Presión media, dp/dt media y kmax/////
    var pm_media= document.getElementById("id_pmax-pm_media");
    var dpdt_media= document.getElementById("id_pmax-dpdt_media");
    var kmax_media= document.getElementById("id_pmax-kmax");

    var pms= document.querySelectorAll(".pm input")
    var dpdt= document.querySelectorAll(".dpdt input")
    var series= document.querySelectorAll(".serie select")

    //Automatizamos las presiones
    function presionMedia(){
        //Sacamos las variables necesarias
        var sumaPresiones= 0;
        var numPresiones= 0;
        var listaValoresMaximos= [0,0,0];
        var listaValores1= [];
        var listaValores2= [];
        var listaValores3= [];
        var valor_maximo= 0.0;

        //Sacamos los valores máximos de cada serie
        pms.forEach(item =>{
            var id_item= item.id;
            var id_serie= id_item.replace("pm_serie", "serie");
            console.log(id_serie)
            var serie= document.getElementById(id_serie);
            var valor_serie= serie.value;

            if(valor_serie=== "1"){
                
                if(item.value){
                    listaValores1.push(item.value);
                }
                
            }

            if(valor_serie=== "2"){
                
                if(item.value){
                    listaValores2.push(item.value);
                }
                
            }

            if(valor_serie=== "3"){
                
                if(item.value){
                    listaValores3.push(item.value);
                }
                
            }          
        })

        if (listaValores1.length > 0){
            listaValoresMaximos[0]= Math.max(...listaValores1);
        }

        if (listaValores2.length > 0){
            listaValoresMaximos[1]= Math.max(...listaValores2);
        }

        if (listaValores3.length > 0){
            listaValoresMaximos[2]= Math.max(...listaValores3);
        }

        console.log(listaValoresMaximos);

        valor_maximo= listaValoresMaximos[0] + listaValoresMaximos[1] + listaValoresMaximos[2];

        //Hacemos la media con el numero de valores que haya
        var numValores= 3;
        listaValoresMaximos.forEach(item =>{    
            if (item === 0){
                numValores= numValores -1;
            }
            pm_media.value= (valor_maximo / numValores).toFixed(2);
        });
        
    };

    //Automatizamos las dPdT
    function dpdtMedia(){
        //Sacamos las variables necesarias
        var sumaPresiones= 0;
        var numPresiones= 0;
        var listaValoresMaximos= [0,0,0];
        var listaValores1= [];
        var listaValores2= [];
        var listaValores3= [];
        var valor_maximo= 0.0;

        //Sacamos los valores máximos de cada serie
        dpdt.forEach(item =>{
            var id_item= item.id;
            var id_serie= id_item.replace("dpdt_serie", "serie");
            var serie= document.getElementById(id_serie);
            var valor_serie= serie.value;

            if(valor_serie=== "1"){
                
                if(item.value){
                    listaValores1.push(item.value);
                }
                
            }

            if(valor_serie=== "2"){
                
                if(item.value){
                    listaValores2.push(item.value);
                }
                
            }

            if(valor_serie=== "3"){
                
                if(item.value){
                    listaValores3.push(item.value);
                }
                
            }          
        })

        if (listaValores1.length > 0){
            listaValoresMaximos[0]= Math.max(...listaValores1);
        }

        if (listaValores2.length > 0){
            listaValoresMaximos[1]= Math.max(...listaValores2);
        }

        if (listaValores3.length > 0){
            listaValoresMaximos[2]= Math.max(...listaValores3);
        }

        console.log(listaValoresMaximos);

        valor_maximo= listaValoresMaximos[0] + listaValoresMaximos[1] + listaValoresMaximos[2];

        //Hacemos la media con el numero de valores que haya
        var numValores= 3;
        listaValoresMaximos.forEach(item =>{    
            if (item === 0){
                numValores= numValores -1;
            }
            dpdt_media.value= parseInt(valor_maximo / numValores);
        });
        
    };

    //Automatizacion kmax
    function kmax(){
        //Hay que aplicar una fórmula que es...
        kmax_media.value= 44;
    };

    //Declaramos los listener

    function listener(){
        console.log("gola");
        pms= document.querySelectorAll(".pm input")
        dpdt= document.querySelectorAll(".dpdt input")
        series= document.querySelectorAll(".serie select")

        pms.forEach(item =>{
            console.log(item);
            item.addEventListener('change', function(){
                presionMedia();
            })
        });
        
        dpdt.forEach(item =>{
            item.addEventListener('change', function(){
                dpdtMedia();
                kmax();
                
            })
        });
        
        series.forEach(item =>{
            item.addEventListener('change', function(){
                presionMedia();
                dpdtMedia();
                kmax();
                
            })
        });
    };


    listener();

    botonAñadir.addEventListener('click', function(){
        listener();  
    })

    botonEliminar.addEventListener('click', function(){
        listener();  
    })
   
});
