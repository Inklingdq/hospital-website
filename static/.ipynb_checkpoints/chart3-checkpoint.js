$(document).ready(function(){      
    var values;
    var legends;
    var labels;
    var predicts;
    $.ajax({
        url:"/get_data",
        type: "get",
        data: {vals: ''},
        success: function(response) {
            full_data = JSON.parse(response.payload);
            values = full_data['values'];
            legends = full_data['legends'];
            labels = full_data['labels'];
            predicts = full_data['predicts'];
        }
    })
      // define the chart data
      var chartData = {
        labels : labels,
        datasets : [{
            label: legends,
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 5,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(75,192,192,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data: values
        }, {
            label: 'prediction',
            fill: false,
            lineTension: 0.1,
            backgroundColor: "rgba(192,75,75,0.4)",
            borderColor: "rgba(192,75,75,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(192,75,75,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 5,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(192,75,75,1)",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
        }]
         }
   
      // get chart canvas
      var ctx = document.getElementById("myChart").getContext("2d");

      // create the chart using the chart canvas
      var myChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {  
           legend: {
            labels: {
                fontColor: "white",
                fontSize: 14
            }
        },   
           scales: {
                        xAxes: [{
                            gridLines: {
        			zeroLineColor:'#fff'
    				},
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Date',
                                fontColor:'#fff',
                                fontSize:15
                            },
                            ticks: {
                               fontColor: "white",
                               fontSize: 15
                              }
                        }],
                        yAxes: [{
                            gridLines: {
        			zeroLineColor: '#fff'
    				},
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: 'Count',
                                fontColor: '#fff',
                                fontSize:15
                            },
                            ticks: {
                                  fontColor: "white",
                                  fontSize: 14
                            }
                        }]
                 },
         }
      });
  });
        