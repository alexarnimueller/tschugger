// member number chart
const memberChart = new Chart(
    document.getElementById('memberChart'),
    {
        type: 'line',
        data: {
            labels: members_years,
            datasets: [{
                label: 'Number of New IAFPA Members',
                backgroundColor: 'rgba(255, 99, 132, 0.25)',
                borderColor: 'rgba(255, 99, 132, 1)',
                data: members_nums,
            }]
        }
    }
);

// payments chart
const paymentChart = new Chart(
    document.getElementById('paymentChart'),
    {
        type: 'line',
        data: {
            labels: payments_years,
            datasets: [{
                type: 'line',
                label: 'Sum of Payments',
                yAxisID: 'y',
                backgroundColor: 'rgba(153, 102, 255, 0.25)',
                borderColor: 'rgba(153, 102, 255, 1)',
                data: payments_sums
            },{
                type: 'bar',
                label: 'Number of Payments',
                yAxisID: 'y2',
                backgroundColor: 'rgba(54, 162, 235, 0.25)',
                borderColor: 'rgba(54, 162, 235, 1)',
                data: payments_nums
            }]
        },
        options: {
            responsive: true,
            scales: {
              y: {
                type: 'linear',
                position: 'left',
                ticks: {
                    color: 'rgba(153, 102, 255, 1)',
                    callback: function(value, index, ticks) {
                        return value + '£';
                    }
                },
                min: 0
              },
              y2: {
                type: 'linear',
                position: 'right',
                ticks: {
                  color: 'rgba(54, 162, 235, 1)'
                },
                grid: {
                  drawOnChartArea: false // only want the grid lines for one axis to show up
                },
                min: 0
              }
            }
        }
    }
);
// categories chart
const categoryChart = new Chart(
    document.getElementById('categoryChart'),
    {
        type: 'doughnut',
        data: {
            labels: categories,
            datasets: [{
                label: 'Number of IAFPA Members',
                data: category_nums,
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 206, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(153, 102, 255)',
                    'rgb(255, 159, 64)',
                    'rgb(15, 68, 50)',
                    'rgb(25, 15, 68)'
                ],
            }]
        }
    }
);


const data = {
  labels: [
    'Red',
    'Blue',
    'Yellow'
  ],
  datasets: [{
    label: 'My First Dataset',
    data: [300, 50, 100],
    backgroundColor: [
      'rgb(255, 99, 132)',
      'rgb(54, 162, 235)',
      'rgb(255, 205, 86)'
    ],
    hoverOffset: 4
  }]
};