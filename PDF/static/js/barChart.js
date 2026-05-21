document.addEventListener("DOMContentLoaded", function () {
    //Datos evolución representa el presente y compariva anual el año pasado
 
    const data = {
        labels: [yearAnterior_json, year_json],
        datasets: [
            {
                label: 'Muestras',
                data: [comparativaAnual.muestras, datosEvolucion.muestras],
                backgroundColor: '#192B5C'
            },
            {
                label: 'Expedientes',
                data: [comparativaAnual.expedientes, datosEvolucion.expedientes, 8],
                backgroundColor: '#2E95AA'
            },
            {
                label: 'Empresas',
                data: [comparativaAnual.empresas, datosEvolucion.empresas, 7],
                backgroundColor: '#5F6B8B'
            }
        ]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            devicePixelRatio: 3,
            layout: {
                padding: {
                    top: 20
                }
            },

            // 👇 CLAVE para Playwright (sin tiempos mágicos)
            animation: {
                onComplete: () => {
                    window.chartRendered = true;
                }
            },

            plugins: {
                legend: {
                    display: true,
                    position: 'bottom'
                },
                datalabels: {
                    anchor: 'center',   // 👈 centrado vertical
                    align: 'center',    // 👈 centrado horizontal
                    color: '#fff',      // 👈 mejor contraste dentro de la barra
                    font: {
                        weight: 'bold'
                    },
                    formatter: function(value) {
                        return value;
                    }
                }
            },

            scales: {
                x: {
                    display: false,
                    grid: {
                        display: false
                    },
                    ticks: {
                        display: false
                    }
                },
                y: {
                    display: false,
                    grid: {
                        display: false
                    },
                    ticks: {
                        display: false
                    }
                }
            }
        },

        plugins: [ChartDataLabels]
    };

    new Chart(document.getElementById('barChart'), config);

});