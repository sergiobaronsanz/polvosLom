//Incio.js
console.log("inicio bien ");

//Cambio periodo
selectorPeriodo= document.getElementById("tipoPeriodo");


selectorPeriodo.addEventListener("change", (e)=>{
    console.log("Hola");
    if (e.target.value === "1"){
        console.log(e.target.value);
    }

    if (e.target.value === "2"){
        console.log(e.target.value);

    }
})