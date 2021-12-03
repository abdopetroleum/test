var ctx = document.getElementById('myChart');
Chart.defaults.global.defaultFontColor = "#fff";
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'data set #1',
                data: [{
                    x: 10,
                    y: 20
                }, {
                    x: 15,
                    y: 10
                }, {
                    x: 25,
                    y: 12.5
                }, {
                    x: 35,
                    y: 7
                }],
                borderColor:
                    '#78C0FF',
                borderWidth: 3
            },
            {
                label: 'data set #2',
                data: [{
                    x: 1,
                    y: 2
                }, {
                    x: 11,
                    y: 25
                }, {
                    x: 21,
                    y: 42
                }, {
                    x: 28,
                    y: 64
                }],
                borderColor:
                    '#E5989B',
                borderWidth: 3
            }]
    },
    options: {
        title: {
            display: true,
            text: 'Chart title x/y',
            fontColor: '#FFF'
        },
        scales: {
            yAxes: [{
                // stacked: true,
                beginAtZero: true
            }],
            xAxes: [{
                type: 'linear',
                position: 'bottom',
                beginAtZero: true
            }]
        }
    }
});