document.addEventListener("DOMContentLoaded", function () {

    const labels = [];
    const dataValues = [];

    top_empresas.forEach(e => {
        labels.push(e.empresa);
        dataValues.push(e.nMuestras);
    });

    const data = {
        labels: labels,
        datasets: [{
            label: 'Muestras',
            data: dataValues,
            backgroundColor: [
                '#007bff',
                '#28a745',
                '#17a2b8',
                '#6c757d',
                '#ffc107'
            ],
            hoverOffset: 4
        }]
    };

    const config = {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Empresas con más muestras'
                }
            }
        }
    };

    const ctx = document.getElementById('myPieChart');

    new Chart(ctx, config);

});