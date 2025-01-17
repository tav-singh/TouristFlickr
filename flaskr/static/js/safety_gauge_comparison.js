
// Based on dom，initial echarts
var myChart = echarts.init(document.getElementById('gauge-comparison'));
// This chart is for comparing three cities' safety
// Specifying configuration items and data for the chart
    var option = {
        title: {
            text: 'Safety Coefficient'
        },
        series : [
            {
                name: '左上转速',
                type: 'gauge',
                center: ['41.6%', '33%'],    // 默认全局居中
                radius: '50%',
                clockwise:true, //仪表盘刻度顺时针增长
                min:0,
                max:100,
                startAngle:240,
                endAngle:60,
                splitNumber:10,
                axisLine: {            // 坐标轴线
                    lineStyle: {       // 属性lineStyle控制线条样式
                        width: 10,
                        color: [[0.2, '#c23531'], [0.8, '#63869e'], [1, '#91c7ae']]
                    }
                },
                axisTick: {            // 坐标轴小标记
                    length:12,        // 属性length控制线长
                    lineStyle: {       // 属性lineStyle控制线条样式
                        color: 'auto'
                    }
                },
                splitLine: {           // 分隔线
                    length:20,         // 属性length控制线长
                    lineStyle: {       // 属性lineStyle（详见lineStyle）控制线条样式
                        color: 'auto'
                    }
                },
                pointer: {
                    width:3
                },
                title: {
                    offsetCenter: ['0', '-20%'],       // x, y，单位px
                    fontSize: 14,
                    color:'gray'
                },
                detail: {
                    offsetCenter: ['0', '20%'],       // x, y，单位px
                    textStyle: {       // 其余属性默认使用全局文本样式
                        fontWeight: 'bolder',
                        fontSize: 18
                    }
                },
                data:[{value: 0, name: 'City A'}]
            },
            {
                name: '右上转速',
                type: 'gauge',
                center: ['58.4%', '33%'],    // 默认全局居中
                radius: '50%',
                min:100,
                max:0,
                startAngle:120,
                endAngle:-60,
                splitNumber:10,
                axisLine: {            // 坐标轴线
                    lineStyle: {       // 属性lineStyle控制线条样式
                        width: 8
                    }
                },
                axisTick: {            // 坐标轴小标记
                    length:12,        // 属性length控制线长
                    lineStyle: {       // 属性lineStyle控制线条样式
                        color: 'auto'
                    }
                },
                splitLine: {           // 分隔线
                    length:20,         // 属性length控制线长
                    lineStyle: {       // 属性lineStyle（详见lineStyle）控制线条样式
                        color: 'auto'
                    }
                },
                pointer: {
                    width:3
                },
                title: {
                    offsetCenter: ['0', '-20%'],       // x, y，单位px
                    fontSize: 14,
                    color:'gray'
                },
                detail: {
                    offsetCenter: ['0', '20%'],       // x, y，单位px
                    textStyle: {       // 其余属性默认使用全局文本样式
                        fontWeight: 'bolder',
                        fontSize: 18
                    }
                },
                data:[{value: 50, name: 'City B'}]
            },
            {
                name: '下转速',
                type: 'gauge',
                center: ['50%', '55%'],    // 默认全局居中
                radius: '50%',
                min:100,
                max:0,
                startAngle:360,
                endAngle:180,
                splitNumber:10,
                axisLine: {            // 坐标轴线
                    lineStyle: {       // 属性lineStyle控制线条样式
                        width: 8
                    }
                },
                axisTick: {            // 坐标轴小标记
                    length:12,        // 属性length控制线长
                    lineStyle: {       // 属性lineStyle控制线条样式
                        color: 'auto'
                    }
                },
                splitLine: {           // 分隔线
                    length:20,         // 属性length控制线长
                    lineStyle: {       // 属性lineStyle（详见lineStyle）控制线条样式
                        color: 'auto'
                    }
                },
                pointer: {
                    width:3
                },
                title: {
                    offsetCenter: ['0', '20%'],       // x, y，单位px
                    fontSize: 14,
                    color:'gray'
                },
                detail: {
                    offsetCenter: ['0', '-10%'],       // x, y，单位px
                    textStyle: {       // 其余属性默认使用全局文本样式
                        fontWeight: 'bolder',
                        fontSize: 18
                    }
                },
                data:[{value: 0, name: 'City C'}]
            },

        ]
    };
myChart.setOption(option);