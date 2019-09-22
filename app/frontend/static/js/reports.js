 $(document).ready(function(){
     function report1(reportLabels, reportData){
      ctx.height = 130;
      var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: reportLabels,//['January', 'February', 'March', 'April', 'May', 'June', 'July'],//
          datasets: [{
            data: reportData,//[78, 81, 80, 45, 34, 12, 40],//
            label: 'Dataset',
            backgroundColor: 'rgba(255,255,255,.1)',
            borderColor: 'rgba(255,255,255,.55)',
          }]
        },
        options: {
          maintainAspectRatio: true,
          legend: {
            display: false
          },
          layout: {
            padding: {
              left: 0,
              right: 0,
              top: 0,
              bottom: 0
            }
          },
          responsive: true,
          scales: {
            xAxes: [{
              gridLines: {
                color: 'transparent',
                zeroLineColor: 'transparent'
              },
              ticks: {
                fontSize: 2,
                fontColor: 'transparent'
              }
            }],
            yAxes: [{
              display: false,
              ticks: {
                beginAtZero: true,
                display: false,
              }
            }]
          },
          title: {
            display: false,
          },
          elements: {
            line: {
              borderWidth: 0
            },
            point: {
              radius: 0,
              hitRadius: 10,
              hoverRadius: 4
            }
          }
        }
      });
        };
        var ctx = document.getElementById("widgetChart01");
        var reportLabels;
        var reportData;
        $.ajax({
            url: '/analytics/report1',
            data: $('form').serialize(),
            type: 'GET',
            success: function(response){
            console.log(ctx);
            result = JSON.parse(response);
            reportLabels = result.labels;//['win-2016','win-2012','win-2003','rhel7','ubuntu14'];//
            reportData = result.values;//[12,24,20,25,17];//
            report1(reportLabels, reportData);
            $("#servers_online").text(result.server_count);
        },
        error: function(error) {
            console.log(error);
        }
        });
     function report2(reportLabels, reportData){
      ctx2.height = 130;
      var myChart = new Chart(ctx2, {
        type: 'bar',
        data: {
          labels: reportLabels,//['January', 'February', 'March', 'April', 'May', 'June', 'July'],//
          datasets: [{
            data: reportData,//[78, 81, 80, 45, 34, 12, 40],//
            label: 'Dataset',
            backgroundColor: 'rgba(255,255,255,.1)',
            borderColor: 'rgba(255,255,255,.55)',
          }]
        },
        options: {
          maintainAspectRatio: true,
          legend: {
            display: false
          },
          layout: {
            padding: {
              left: 0,
              right: 0,
              top: 0,
              bottom: 0
            }
          },
          responsive: true,
          scales: {
            xAxes: [{
              gridLines: {
                color: 'transparent',
                zeroLineColor: 'transparent'
              },
              ticks: {
                fontSize: 2,
                fontColor: 'transparent'
              }
            }],
            yAxes: [{
              display: false,
              ticks: {
                beginAtZero: true,
                display: false,
              }
            }]
          },
          title: {
            display: false,
          },
          elements: {
            line: {
              borderWidth: 0
            },
            point: {
              radius: 0,
              hitRadius: 10,
              hoverRadius: 4
            }
          }
        }
      });
        };
        var ctx2 = document.getElementById("widgetChart02");
        var reportLabels2;
        var reportData2;
        $.ajax({
            url: '/analytics/report2',
            data: $('form').serialize(),
            type: 'GET',
            success: function(response){
            console.log(ctx);
            result = JSON.parse(response);
            reportLabels2 = result.task_status;//['win-2016','win-2012','win-2003','rhel7','ubuntu14'];//
            reportData2 = result.values;//[12,24,20,25,17];//
            report2(reportLabels2, reportData2);
            $("#tasks_status").text(result.tasks_count);
        },
        error: function(error) {
            console.log(error);
        }
    });
    function report3(reportLabels, reportData){
      ctx.height = 130;
      var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: reportLabels,//['January', 'February', 'March', 'April', 'May', 'June', 'July'],//
          datasets: [{
            data: reportData,//[78, 81, 80, 45, 34, 12, 40],//
            label: 'Dataset',
            backgroundColor: 'rgba(255,255,255,.1)',
            borderColor: 'rgba(255,255,255,.55)',
          }]
        },
        options: {
          maintainAspectRatio: true,
          legend: {
            display: false
          },
          layout: {
            padding: {
              left: 0,
              right: 0,
              top: 0,
              bottom: 0
            }
          },
          responsive: true,
          scales: {
            xAxes: [{
              gridLines: {
                color: 'transparent',
                zeroLineColor: 'transparent'
              },
              ticks: {
                fontSize: 2,
                fontColor: 'transparent'
              }
            }],
            yAxes: [{
              display: false,
              ticks: {
                beginAtZero: true,
                display: false,
              }
            }]
          },
          title: {
            display: false,
          },
          elements: {
            line: {
              borderWidth: 0
            },
            point: {
              radius: 0,
              hitRadius: 10,
              hoverRadius: 4
            }
          }
        }
      });
        };
        var ctx = document.getElementById("widgetChart03");
        var reportLabels3;
        var reportData3;
        $.ajax({
            url: '/analytics/report3',
            data: $('form').serialize(),
            type: 'GET',
            success: function(response){
            console.log(ctx);
            result = JSON.parse(response);
            reportLabels3 = result.labels;//['win-2016','win-2012','win-2003','rhel7','ubuntu14'];//
            reportData3 = result.values;//[12,24,20,25,17];//
            report3(reportLabels3, reportData3);
            $("#job_status").text(result.server_count);
        },
        error: function(error) {
            console.log(error);
        }
        });
    });
