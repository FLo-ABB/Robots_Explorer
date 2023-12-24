var ctx = document.getElementById("chart").getContext("2d");
var myChart = new Chart(ctx, {
    type: "scatter",
    options: {
        animation: {
            duration: 0
        },
        title: {
            display: false
        },
        plugins: {
            legend: {
                display: false,
                labels: {
                    display: false
                }
            },
            zoom: {
                zoom: {
                    wheel: {
                        enabled: true
                    },
                    pinch: {
                        enabled: true
                    },
                    mode: 'xy'
                },
                pan: {
                    enabled: true,
                    mode: 'xy'
                }
            },
            maintainAspectRatio: false
        },
        scales: {
            x: {
                type: 'logarithmic',
                title: {
                    display: true,
                    text: 'Reach (mm)'
                },
                ticks: {
                    min: 200,
                    max: 5000
                }
            },
            y: {
                type: 'logarithmic',
                title: {
                    display: true,
                    text: 'Payload (kg)'
                },
                ticks: {
                    min: 0.3,
                    max: 3000
                }
            }
        },
    }
});

function drawChart() {
    var brands = [];
    var checkboxes = document.querySelectorAll("#checkboxContainer input[type='checkbox']:checked");
    for (var i = 0; i < checkboxes.length; i++) {
        brands.push(checkboxes[i].value);
    }
    var spans = document.querySelectorAll("#checkboxContainer span");
    for (var i = 0; i < spans.length; i++) {
        if (brands.indexOf(spans[i].previousSibling.value) == -1) {
            spans[i].style.backgroundColor = "rgba(0, 0, 0, 0)";
        } else {
            spans[i].style.backgroundColor = robotColor(spans[i].previousSibling.value);
        }
    }
    var datasets = [];
    for (var i = 0; i < brands.length; i++) {
        datasets = datasets.concat(getDatasets(brands[i]));
    }
    myChart.data.datasets = datasets;
    myChart.update();
}


function robotColor(brand) {
    const colors = {
        "ABB": "rgba(235, 235, 235, 1)",
        "KUKA": "rgba(255, 92, 0, 1)",
        "Fanuc": "rgba(254, 209, 0, 1)",
        "Yaskawa Motoman": "rgba(1, 93, 170, 1)",
        "Staubli": "rgba(150, 154, 156, 1)",
        "Universal Robots": "rgba(86, 160, 211, 1)"
    };

    return colors[brand] || "rgba(255, 99, 132, 1)";
}

function createSpanForCheckbox(checkbox) {
    var span = document.createElement("span");
    span.style.width = "10px";
    span.style.height = "10px";
    span.style.borderRadius = "50%";
    span.style.display = "inline-block";
    span.style.margin = "3px";
    checkbox.parentNode.insertBefore(span, checkbox.nextSibling);
}
var checkboxes = document.querySelectorAll("#checkboxContainer input[type='checkbox']");
for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].addEventListener("change", drawChart);
    createSpanForCheckbox(checkboxes[i]);
}

function highlightOnChart(robotName) {
    var datasets = myChart.data.datasets;
    var xValue, yValue;

    for (var i = 0; i < datasets.length; i++) {
        if (datasets[i].label == robotName) {
            xValue = datasets[i].data[0].x;
            yValue = datasets[i].data[0].y;
        }
    }

    myChart.options.plugins.annotation = {
        annotations: {
            line1: {
                type: 'line',
                scaleID: 'x',
                value: xValue,
                borderDash: [5, 5],
                borderColor: 'rgba(0,23,23,1)',
                borderWidth: 1
            },
            line2: {
                type: 'line',
                scaleID: 'y',
                value: yValue,
                borderDash: [5, 5],
                borderColor: 'rgba(0,23,23,1)',
                borderWidth: 1
            }
        }
    };

    myChart.update();
}

drawChart();