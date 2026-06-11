document.addEventListener("DOMContentLoaded", function () {
    const width = 600;
    const height = 410;

    const svg = d3.select("#mapa")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .style("transform", "scale(0.90)")
        .style("transform-origin", "top left");

    
    const maxValue = Math.max(...Object.values(procedencia_muestras_json));

    // escala de color
    const color = d3.scaleSequential()
        .domain([0, maxValue])
        .interpolator(d3.interpolateBlues);


    //Normalizar nombres
    function normalizarProvincia(nombre) {
        nombre = nombre.toLowerCase();

        if (nombre === "valència/valencia") return "valencia";
        if (nombre === "alacant/alicante") return "alicante";
        if (nombre === "castelló/castellón") return "castellon";
        if (nombre === "bizkaia/vizcaya") return "vizcaya";
        if (nombre === "gipuzkoa/guipúzcoa") return "guipuzcoa";
        if (nombre === "araba/álava") return "alava";

        return nombre;
    }

    // proyección centrada en península
    const projection = d3.geoMercator()
        .center([-3.5, 40.2])
        .scale(2200)
        .translate([width / 2, height / 2]);

    const path = d3.geoPath().projection(projection);

    geojson.features.forEach(d => {
        const name = normalizarProvincia(d.properties.name);

        d.properties.value = procedencia_muestras_json[name] || 0;
    });

    svg.selectAll("path")
        .data(geojson.features)
        .enter()
        .append("path")
        .attr("d", function(d) {

            const name = d.properties.name.toLowerCase();

            // Canarias movidas manualmente
            if (
                name.includes("palmas") ||
                name.includes("santa cruz de tenerife")
            ) {

                const canariasPath = d3.select(this);

                // dibujar normalmente
                const original = path(d);

                // crear path temporal
                canariasPath.attr("d", original);

                // mover y reducir
                canariasPath.attr(
                    "transform",
                    "translate(-250,250) scale(0.7)"
                );

                return original;
            }

            return path(d);
        })
        .attr("fill", d => color(d.properties.value))
        .attr("stroke", "#000")
        .attr("stroke-width", 0.5);
});