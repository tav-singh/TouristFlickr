// Based on dom，initial echarts
var myChart = echarts.init(document.getElementById('summary-comparison'));
//show the safety coefficient for the chosen city
// Specifying configuration items and data for the chart
var option = {
    title: {
        text: 'Summary'
    },
    tooltip: {},
    legend: {
        data: ['city 1', 'city 2' ,'city 3']
    },
    radar: {
        // shape: 'circle',
        name: {
            textStyle: {
                color: '#fff',
                backgroundColor: '#999',
                borderRadius: 3,
                padding: [3, 5]
            }
        },
        indicator: [
            { name: 'Restaurant Price Index', max:486},
            { name: 'Groceries Index', max:486},
            { name: 'Cost of Living Index', max:486},
            { name: 'Traffic Index', max:486},
            { name: 'Time Index', max:486},

        ]
    },
    series: [{
        type: 'radar',
        // areaStyle: {normal: {}},
        data: [
            {
                value: [60.82, 96.02, 114.57, 115.81, 99.42],//traffic_index from 2015 to 2019!!!
                name: 'city 1'
            },
            {
                value: [27, 31, 35.97, 36, 32.08],//traffic_index from 2015 to 2019
                name: 'city '
            },
            {
                value: [39.04, 97.04, 105.55, 105.91, 80.43],//traffic_index from 2015 to 2019
                name: 'city 3'
            }
        ]
    }]
};
myChart.setOption(option);