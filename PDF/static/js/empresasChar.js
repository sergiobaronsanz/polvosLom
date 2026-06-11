document.addEventListener("DOMContentLoaded", function () {

    console.log(top_empresas_json);
    console.log(typeof top_empresas_json);
    console.log(top_empresas_json);
    console.log(top_empresas_json[0]);

    Chart.register(ChartDataLabels);

    const labels = top_empresas_json.map(e => e.empresa);
    const dataEmpresas = top_empresas_json.map(e => e.total_muestras);

    const colors = [
        '#1E3A8A',
        '#2255A0',
        '#266FB4',
        '#2B84B4',
        '#2E95AA'
    ];

    const baseOptions = {

        responsive: true,
        maintainAspectRatio: false,
        devicePixelRatio: 3,

        indexAxis: 'y', // 👉 horizontal

        layout: {
            padding: {
                top: 10,
                right: 20,
                bottom: 10,
                left: 10
            }
        },

        animation: {
            duration: 0,
            onComplete: () => {
                window.chartRendered = true;
            }
        },

        plugins: {

            legend: {
                display: false
            },

            tooltip: {
                enabled: true
            },

            datalabels: {

                anchor: 'end',
                align: 'right',

                color: '#111827',

                font: {
                    weight: 'bold',
                    size: 12
                },

                formatter: (value) => value
            }
        },

        scales: {

            x: {

                beginAtZero: true,

                grid: {
                    color: '#E5E7EB'
                },

                ticks: {
                    color: '#6B7280',
                    font: {
                        size: 11
                    }
                },

                border: {
                    display: false
                }
            },

            y: {

                grid: {
                    display: false
                },

                ticks: {
                    color: '#111827',

                    font: {
                        size: 12,
                        weight: '600'
                    }
                },

                border: {
                    display: false
                }
            }
        }
    };

    // 👉 BAR CHART HORIZONTAL
    new Chart(document.getElementById('empresasChar'), {

        type: 'bar',

        data: {

            labels: labels,

            datasets: [{
                data: dataEmpresas,

                backgroundColor: colors,
                borderRadius: 8,
                borderSkipped: false,
                barThickness: 18
            }]
        },

        options: baseOptions
    });

});