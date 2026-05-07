document.addEventListener("DOMContentLoaded", function () {

    Chart.register(ChartDataLabels);

    const labels = [];
    const dataEnsayos = [];

    const tipo_empresas = [
        { empresa: "Nuevas", nEmpresas: 25 },
        { empresa: "Recurrentes", nEmpresas: 72 },
    ];

    const total = tipo_empresas.reduce(
        (acc, e) => acc + e.nEmpresas,
        0
    );

    tipo_empresas.forEach(e => {

        labels.push(
            `${e.empresa} (${e.nEmpresas})`
        );

        dataEnsayos.push(e.nEmpresas);
    });

    const colors = [
        '#1E3A8A',
        '#2E95AA',
    ];

    // 👉 Plugin texto central
    const centerTextPlugin = {

        id: 'centerText',

        beforeDraw(chart) {

            const { ctx, chartArea } = chart;

            if (!chartArea) return;

            const { top, bottom, left, right } = chartArea;

            const centerX = (left + right) / 2;
            const centerY = (top + bottom) / 2;

            ctx.save();

            // 👉 Número principal
            ctx.font = 'bold 28px Arial';
            ctx.fillStyle = '#111827';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            ctx.fillText(total, centerX, centerY - 10);

            // 👉 Texto inferior
            ctx.font = '14px Arial';
            ctx.fillStyle = '#6B7280';

            ctx.fillText('empresas', centerX, centerY + 18);

            ctx.restore();
        }
    };

    

    const baseOptions = {

        responsive: true,
        maintainAspectRatio: false,
        devicePixelRatio: 3,
        cutout: '70%',

        layout: {
            padding: {
                top: 0,
                bottom: 10,
            }
        },

        animation: {
            duration: 0,
            onComplete: () => {
                window.chartRendered = true;
            }
        },

        plugins: {

            // 👉 Leyenda abajo
            legend: {

                display: true,
                position: 'right',

                labels: {

                    usePointStyle: true,
                    pointStyle: 'circle',
                    padding: 20,

                    font: {
                        size: 13
                    },

                    color: '#374151'
                }
            },

            datalabels: {
                display: false
            }
        }
    };

    // 👉 DONUT
    new Chart(document.getElementById('donut'), {

        type: 'doughnut',

        data: {

            labels: labels,

            datasets: [{
                data: dataEnsayos,
                backgroundColor: colors,
                hoverOffset: 4,
                borderWidth: 0
            }]
        },

        options: baseOptions,

        plugins: [centerTextPlugin] 
    });

});