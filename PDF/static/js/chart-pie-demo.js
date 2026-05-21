document.addEventListener("DOMContentLoaded", function () {

    Chart.register(ChartDataLabels);

    const labels = [];
    const dataEnsayos = [];
    const dataHoras = [];
    const colors = [];

    // 👉 Datos desde Django
    calculosEnsayos.ensayosOrdenados.forEach(e => {

        labels.push(e.nombre);
        dataEnsayos.push(e.ensayos);
        dataHoras.push(e.horas);
        colors.push(e.color);

    });

    const centerTextPlugin = {

        id: 'centerText',

        beforeDraw(chart) {

            const { ctx, chartArea } = chart;

            if (!chartArea) return;

            const { top, bottom, left, right } = chartArea;

            const centerX = (left + right) / 2;
            const centerY = (top + bottom) / 2;

            // 👉 total dinámico
            const total = chart.data.datasets[0].data
                .reduce((a, b) => a + b, 0);

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

            const text = chart.canvas.id === 'myPieChart'
                ? 'ensayos'
                : 'horas';

            ctx.fillText(text, centerX, centerY + 18);

            ctx.restore();
        }
    };

    const baseOptions = {

        responsive: true,
        devicePixelRatio: 3,

        layout: {
            padding: {
                top: 0
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

            datalabels: {
                display: false
            }

        }

    };

    // 👉 ENSAYOS
    new Chart(document.getElementById('myPieChart'), {

        type: 'doughnut',

        data: {
            labels: labels,
            datasets: [{
                data: dataEnsayos,
                backgroundColor: colors,
                hoverOffset: 4
            }]
        },

        options: baseOptions,

        plugins: [centerTextPlugin],

    });

    // 👉 HORAS
    new Chart(document.getElementById('myPieChart_2'), {

        type: 'doughnut',

        data: {
            labels: labels,
            datasets: [{
                data: dataHoras,
                backgroundColor: colors,
                hoverOffset: 4
            }]
        },

        options: baseOptions,

        plugins: [centerTextPlugin]

    });

    // 👉 LEYENDA
    const legendContainer = document.getElementById('customLegend');

    calculosEnsayos.ensayosOrdenados.forEach((e) => {

        const item = document.createElement('div');

        item.style.display = 'flex';
        item.style.alignItems = 'center';
        item.style.gap = '6px';

        const colorBox = document.createElement('span');

        colorBox.style.width = '12px';
        colorBox.style.height = '12px';
        colorBox.style.backgroundColor = e.color;
        colorBox.style.borderRadius = '50%';

        const text = document.createElement('span');

        text.textContent = `${e.nombre} (${e.porcentaje}%)`;
        text.style.fontSize = '12px';

        item.appendChild(colorBox);
        item.appendChild(text);

        legendContainer.appendChild(item);

    });

});