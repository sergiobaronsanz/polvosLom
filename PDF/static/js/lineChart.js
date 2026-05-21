document.addEventListener("DOMContentLoaded", function () {

    const data = {
        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
        datasets: [
            {
                label: 'Muestras',
                data: muestrasMensual,
                borderColor: '#192B5C',
                backgroundColor: '#192B5C',
                fill: false,
                tension: 0.3
            },
            {
                label: 'Expedientes',
                data: expedientesMensual,
                borderColor: '#2E95AA',
                backgroundColor: '#2E95AA',
                fill: false,
                tension: 0.3
            },
        ]
    };

    const config = {
        type: 'line', // 👈 cambiado
        data: data,
        options: {
            responsive: true,
            devicePixelRatio: 3,

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
                    anchor: 'end',
                    align: 'top',
                    color: '#000',
                    font: {
                        weight: 'bold'
                    }
                }
            },

            scales: {
                x: {
                    display: true,
                    grid: {
                        display: false // ❌ quita líneas verticales
                    }
                },
                y: {
                    display: true,
                    grid: {
                        display: false // ❌ quita líneas horizontales
                    },
                    ticks: {
                        stepSize: 5
                    }
                }
            }
        },
    };

    new Chart(document.getElementById('lineChart'), config);

});