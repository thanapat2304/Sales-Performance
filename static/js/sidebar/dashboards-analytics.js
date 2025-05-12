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

document.addEventListener('DOMContentLoaded', function() {
  const donutValue = document.getElementById('growthChart1').getAttribute('data-donut-value');
  const targetValue = document.getElementById('growthChart1').getAttribute('data-target-value');
  
  const growthChartEl = document.querySelector('#growthChart1');
  const growthChartOptions = {
      series: [parseFloat(donutValue)],
      labels: ['Achieve'],
      chart: {
          height: 240,
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
      colors: [config.colors.primary],
      fill: {
        type: 'solid',
        color: config.colors.primary
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

  // Order Statistics Chart
  // --------------------------------------------------------------------
  const chartOrderStatistics = document.querySelector('#orderStatisticsChart');

  if (chartOrderStatistics) {
    fetch('/get-chart-data')
      .then(response => response.json())
      .then(data => {
        if (data.labels.length !== data.series.length) {
          console.error('Mismatch between labels and series length');
          return;
        }
  
        const orderChartConfig = {
          chart: {
            height: 165,
            width: 200,
            type: 'donut'
          },
          labels: data.labels,
          series: data.series,
          colors: [
            '#FF5733',
            '#33FF57',
            '#3357FF',
            '#F1C40F',
            '#8E44AD',
            '#1ABC9C',
            '#E74C3C',
            '#3498DB',
            '#F39C12',
            '#9B59B6',
            '#2ECC71',
            '#FF9FF3',
            '#00d2d3',
            '#576574'
          ],
          stroke: {
            width: 5,
            colors: ['#fff']
          },
          dataLabels: {
            enabled: false
          },
          legend: {
            show: false
          },
          grid: {
            padding: {
              top: 0,
              bottom: 0,
              right: 15
            }
          },
          plotOptions: {
            pie: {
              donut: {
                size: '65%',
                labels: {
                  show: true,
                  value: {
                    fontSize: '1rem',
                    fontFamily: 'Public Sans',
                    color: '#000',
                    offsetY: -15
                  },
                  name: {
                    offsetY: 20,
                    fontFamily: 'Public Sans'
                  }
                }
              }
            }
          }
        };
  
        const statisticsChart = new ApexCharts(chartOrderStatistics, orderChartConfig);
        statisticsChart.render();
      })
      .catch(error => console.error('Error fetching chart data:', error));
  }  

  const chartSaleStatistics = document.querySelector('#saleStatisticsChart');

  const smcode = window.location.pathname.split('/').pop();
  
  if (chartSaleStatistics) {
    fetch(`/get-chart-data-sale/${smcode}`)
      .then(response => response.json())
      .then(data => {
        if (data.labels.length !== data.series.length) {
          console.error('Mismatch between labels and series length');
          return;
        }
  
        const saleChartConfig = {
          chart: {
            height: 165,
            width: 200,
            type: 'donut'
          },
          labels: data.labels,
          series: data.series,
          colors: [
            '#FF5733',
            '#33FF57',
            '#3357FF',
            '#F1C40F',
            '#8E44AD',
            '#1ABC9C',
            '#E74C3C',
            '#3498DB',
            '#F39C12',
            '#9B59B6',
            '#2ECC71',
            '#FF9FF3',
            '#00d2d3',
            '#576574'
          ],
          stroke: {
            width: 5,
            colors: ['#fff']
          },
          dataLabels: {
            enabled: false
          },
          legend: {
            show: false
          },
          grid: {
            padding: {
              top: 0,
              bottom: 0,
              right: 15
            }
          },
          plotOptions: {
            pie: {
              donut: {
                size: '65%',
                labels: {
                  show: true,
                  value: {
                    fontSize: '1rem',
                    fontFamily: 'Public Sans',
                    color: '#000',
                    offsetY: -15
                  },
                  name: {
                    offsetY: 20,
                    fontFamily: 'Public Sans'
                  }
                }
              }
            }
          }
        };
  
        const saleChart = new ApexCharts(chartSaleStatistics, saleChartConfig);
        saleChart.render();
      })
      .catch(error => console.error('Error fetching chart data for sale:', error));
  }

  // Income Chart - Area chart
  // --------------------------------------------------------------------
  const incomeChartEl = document.querySelector('#incomeChart');

  fetch('/get_monthly_data')
    .then(response => response.json())
    .then(data => {

      const currentYear = new Date().getFullYear();
      const previousYear = currentYear - 1;
      const twoYearsAgo = currentYear - 2;
      const incomeChartConfig = {
        series: [
          {
            name: `${currentYear}`,
            data: data['now']
          },
          {
            name: `${previousYear}`,
            data: data['one_year']
          },
          {
            name: `${twoYearsAgo}`,
            data: data['two_year']
          }
        ],
        chart: {
          height: 315,
          parentHeightOffset: 0,
          parentWidthOffset: 0,
          toolbar: {
            show: false
          },
          type: 'area'
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          width: 2,
          curve: 'smooth'
        },
        legend: {
          show: true
        },
        markers: {
          size: 6,
          colors: 'transparent',
          strokeColors: 'transparent',
          strokeWidth: 4,
          hover: {
            size: 7
          }
        },
        colors: ['#71dd37', '#03c3ec', '#696cff'],
        fill: {
          type: 'gradient',
          gradient: {
            shade: 'light',
            shadeIntensity: 0.6,
            opacityFrom: 0.5,
            opacityTo: 0.25,
            stops: [0, 95, 100]
          }
        },
        grid: {
          borderColor: '#e0e0e0',
          strokeDashArray: 3,
          padding: {
            top: -20,
            bottom: -8,
            left: -10,
            right: 8
          }
        },
        xaxis: {
          categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false
          },
          labels: {
            show: true,
            style: {
              fontSize: '13px',
              colors: '#697a8d'
            }
          }
        },
        tooltip: {
          y: {
            formatter: function (value) {
              if (value === null) {
                return '-';
              }
              return value.toLocaleString();
            }
          }
        }
      };      
  
      if (typeof incomeChartEl !== undefined && incomeChartEl !== null) {
        const incomeChart = new ApexCharts(incomeChartEl, incomeChartConfig);
        incomeChart.render();
      }
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });

    const incomeChartEl1 = document.querySelector('#OverChart');

    fetch('/get_monthly_over')
      .then(response => response.json())
      .then(data => {
  
        const currentYear = new Date().getFullYear();
        const previousYear = currentYear - 1;
        const twoYearsAgo = currentYear - 2;
        const incomeChartConfig = {
          series: [
            {
              name: `${currentYear}`,
              data: data['now']
            },
            {
              name: `${previousYear}`,
              data: data['one_year']
            },
            {
              name: `${twoYearsAgo}`,
              data: data['two_year']
            }
          ],
          chart: {
            height: 315,
            parentHeightOffset: 0,
            parentWidthOffset: 0,
            toolbar: {
              show: false
            },
            type: 'area'
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            width: 2,
            curve: 'smooth'
          },
          legend: {
            show: true
          },
          markers: {
            size: 6,
            colors: 'transparent',
            strokeColors: 'transparent',
            strokeWidth: 4,
            hover: {
              size: 7
            }
          },
          colors: ['#71dd37', '#03c3ec', '#696cff'],
          fill: {
            type: 'gradient',
            gradient: {
              shade: 'light',
              shadeIntensity: 0.6,
              opacityFrom: 0.5,
              opacityTo: 0.25,
              stops: [0, 95, 100]
            }
          },
          grid: {
            borderColor: '#e0e0e0',
            strokeDashArray: 3,
            padding: {
              top: -20,
              bottom: -8,
              left: -10,
              right: 8
            }
          },
          xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            axisBorder: {
              show: false
            },
            axisTicks: {
              show: false
            },
            labels: {
              show: true,
              style: {
                fontSize: '13px',
                colors: '#697a8d'
              }
            }
          },
          tooltip: {
            y: {
              formatter: function (value) {
                if (value === null) {
                  return '-';
                }
                return value.toLocaleString();
              }
            }
          }
        };      
    
        if (typeof incomeChartEl1 !== undefined && incomeChartEl1 !== null) {
          const incomeChart = new ApexCharts(incomeChartEl1, incomeChartConfig);
          incomeChart.render();
        }
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });

// กราฟสำหรับข้อมูลการขาย
const saleChartEl = document.querySelector('#saleChart');
const smcode1 = window.location.pathname.split('/').pop();

if (saleChartEl) {
  fetch(`/get_monthly_data_sale/${smcode1}`)
    .then(response => response.json())
    .then(data => {
      const currentYear = new Date().getFullYear();
      const previousYear = currentYear - 1;
      const twoYearsAgo = currentYear - 2;
      const saleChartConfig = {
        series: [
          {
            name: `${currentYear}`,
            data: data['now']
          },
          {
            name: `${previousYear}`,
            data: data['one_year']
          },
          {
            name: `${twoYearsAgo}`,
            data: data['two_year']
          }
        ],
        chart: {
          height: 315,
          parentHeightOffset: 0,
          parentWidthOffset: 0,
          toolbar: {
            show: false
          },
          type: 'area'
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          width: 2,
          curve: 'smooth'
        },
        legend: {
          show: true
        },
        markers: {
          size: 6,
          colors: 'transparent',
          strokeColors: 'transparent',
          strokeWidth: 4,
          hover: {
            size: 7
          }
        },
        colors: ['#71dd37', '#03c3ec', '#696cff'],
        fill: {
          type: 'gradient',
          gradient: {
            shade: 'light',
            shadeIntensity: 0.6,
            opacityFrom: 0.5,
            opacityTo: 0.25,
            stops: [0, 95, 100]
          }
        },
        grid: {
          borderColor: '#e0e0e0',
          strokeDashArray: 3,
          padding: {
            top: -20,
            bottom: -8,
            left: -10,
            right: 8
          }
        },
        xaxis: {
          categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false
          },
          labels: {
            show: true,
            style: {
              fontSize: '13px',
              colors: '#697a8d'
            }
          }
        },
        tooltip: {
          y: {
            formatter: function (value) {
              if (value === null) {
                return '-';
              }
              return value.toLocaleString();
            }
          }
        }
      };

      const saleChart = new ApexCharts(saleChartEl, saleChartConfig);
      saleChart.render();
    })
    .catch(error => {
      console.error('Error fetching sale data:', error);
    });
}
  if (typeof weeklyExpensesEl !== undefined && weeklyExpensesEl !== null) {
    const weeklyExpenses = new ApexCharts(weeklyExpensesEl, weeklyExpensesConfig);
    weeklyExpenses.render();
  }
})();
