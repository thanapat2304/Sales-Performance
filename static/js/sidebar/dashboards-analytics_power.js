/**
 * Dashboard Analytics
 */

'use strict';

(function () {
  let cardColor, headingColor, axisColor, shadeColor, borderColor;

  cardColor = config.colors.white;
  headingColor = config.colors.headingColor;
  axisColor = config.colors.axisColor;
  borderColor = config.colors.borderColor;

  // Growth Chart - Radial Bar Chart
  // --------------------------------------------------------------------
  document.addEventListener('DOMContentLoaded', function() {
    const donutValue = document.getElementById('growthChart').getAttribute('data-donut-value');
    const targetValue = document.getElementById('growthChart').getAttribute('data-target-value');
    
    const growthChartEl = document.querySelector('#growthChart');
    const growthChartOptions = {
        series: [parseFloat(donutValue)],
        labels: ['Achieve'],
        chart: {
            height: 190,
            type: 'radialBar'
        },
        plotOptions: {
            radialBar: {
                size: 150,
                offsetY: 10,
                startAngle: -150,
                endAngle: 150,
                hollow: {
                    size: '55%'
                },
                track: {
                    background: 'rgba(232, 234, 235, 0.4)',
                    strokeWidth: '100%'
                },
                dataLabels: {
                    name: {
                        offsetY: 15,
                        color: headingColor,
                        fontSize: '15px',
                        fontWeight: '600',
                        fontFamily: 'Public Sans'
                    },
                    value: {
                        offsetY: -25,
                        color: headingColor,
                        fontSize: '22px',
                        fontWeight: '500',
                        fontFamily: 'Public Sans',
                        formatter: function() {
                            return targetValue;
                        }
                    }
                }
            }
        },
        colors: [config.colors.warning],
        fill: {
          type: 'solid',
          color: config.colors.warning
        },
        stroke: {
            dashArray: 5
        },
        grid: {
            padding: {
                top: -35,
                bottom: -10
            }
        },
        states: {
            hover: {
                filter: {
                    type: 'none'
                }
            },
            active: {
                filter: {
                    type: 'none'
                }
            }
        }
    };

    if (typeof growthChartEl !== undefined && growthChartEl !== null) {
        const growthChart = new ApexCharts(growthChartEl, growthChartOptions);
        growthChart.render();
    }
});

  if (typeof weeklyExpensesEl !== undefined && weeklyExpensesEl !== null) {
    const weeklyExpenses = new ApexCharts(weeklyExpensesEl, weeklyExpensesConfig);
    weeklyExpenses.render();
  }
})();
