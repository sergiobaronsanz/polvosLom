document.addEventListener("DOMContentLoaded", function () {

    const data = {
        labels: ['2025', '2026'],
        datasets: [
            {
                label: 'Muestras',
                data: [17, 30],
                backgroundColor: '#192B5C'
            },
            {
                label: 'Expedientes',
                data: [7, 8],
                backgroundColor: '#5F6B8B'
            },
            {
                label: 'Empresas',
                data: [3, 7],
                backgroundColor: '#2E95AA'
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
                    top: 5
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
                    anchor: 'end',
                    align: 'end',
                    offset: 4,
                    color: '#000',
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