console.log("hola luisito");

//Variables comunes
var botonTodoNegativo=document.getElementById("todoNegativo");
var selectsTabla= document.querySelectorAll("#tabla select");


//Todo negativo
function todoNegativo(){
    botonTodoNegativo.addEventListener("click",function(){
        selectsTabla.forEach(select => {
            select.value= "2";
            
        });
    })
}

todoNegativo();