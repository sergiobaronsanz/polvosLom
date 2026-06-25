document.addEventListener('DOMContentLoaded', function() {
    const selectorFuente = document.getElementById("id_bz-tipoFuenteIgnicion");
    const selectorTiempo = document.getElementById("id_bz-tiempoFuenteIgnicion");

    const selectorCombustion = document.getElementById("id_bz-tipoIgnicion");
    const selectorResultado = document.getElementById("id_bz-resultado");

    function actualizarTiempo() {
        selectorTiempo.value = selectorFuente.value === "1" ? 5 : 2;
    }

    function actualizarResultado() {
        selectorResultado.value = selectorCombustion.value;
    }

    function actualizarCombustion() {
        selectorCombustion.value = selectorResultado.value;
    }

    actualizarTiempo();
    actualizarResultado();

    //Se actualize uno u otro, cambian los 2
    selectorFuente.addEventListener("change", actualizarTiempo);
    selectorCombustion.addEventListener("change", actualizarResultado);
    selectorResultado.addEventListener("change", actualizarCombustion);


});