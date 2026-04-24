document.addEventListener("DOMContentLoaded", function () {

    Chart.register(ChartDataLabels);

    const labels = [];
    const dataEnsayos = [];
    const dataHoras = [];

    const top_empresas = [
        { ensayo: "TMIc", nEnsayos: 25, horas: 120 },
        { ensayo: "TMIn", nEnsayos: 18, horas: 95 },
        { ensayo: "EMI", nEnsayos: 12, horas: 60 },
        { ensayo: "LIE", nEnsayos: 9, horas: 40 },
        { ensayo: "PMAX", nEnsayos: 6, horas: 90 },
        { ensayo: "REC", nEnsayos: 6, horas: 28 },
        { ensayo: "CLO", nEnsayos: 6, horas: 25 },
        { ensayo: "N1", nEnsayos: 6, horas: 22 },
        { ensayo: "N2", nEnsayos: 6, horas: 20 },
        { ensayo: "N4", nEnsayos: 6, horas: 18 },
        { ensayo: "O1", nEnsayos: 6, horas: 15 },
    ];

    top_empresas.forEach(e => {
        labels.push(e.ensayo);
        dataEnsayos.push(e.nEnsayos);
        dataHoras.push(e.horas);
    });

    const colors = [
        '#1E3A8A',
        '#2563EB',
        '#3B82F6',
        '#60A5FA',
        '#93C5FD',
        '#2E95AA',
        '#14B8A6',
        '#22C55E',
        '#84CC16',
        '#F59E0B',
        '#EF4444'
    ];

    const baseOptions = {
        responsive: true,
        devicePixelRatio: 3,
        layout: { padding: { top: 0 } },
        animation: {
            duration: 0, 
            onComplete: () => {
                window.chartRendered = true;
            }
        },
        plugins: {
            legend: { display: false }, // 👈 una sola leyenda externa
            datalabels: {
                display: false
            }
        }
    };

    // 👉 ENSAYOS (izquierda)
    new Chart(document.getElementById('myPieChart'), {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: dataEnsayos,
                backgroundColor: colors,
                hoverOffset: 4
            }]
        },
        options: baseOptions
    });

    // 👉 HORAS (derecha)
    new Chart(document.getElementById('myPieChart_2'), {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: dataHoras,
                backgroundColor: colors,
                hoverOffset: 4
            }]
        },
        options: baseOptions
    });

    // 👉 LEYENDA CENTRAL COMPARTIDA
    const legendContainer = document.getElementById('customLegend');

    labels.forEach((label, i) => {
        const item = document.createElement('div');
        item.style.display = 'flex';
        item.style.alignItems = 'center';
        item.style.gap = '6px';

        const colorBox = document.createElement('span');
        colorBox.style.width = '12px';
        colorBox.style.height = '12px';
        colorBox.style.backgroundColor = colors[i];

        const text = document.createElement('span');
        text.textContent = label;
         text.style.fontSize = '12px';

        item.appendChild(colorBox);
        item.appendChild(text);
        legendContainer.appendChild(item);
    });

});