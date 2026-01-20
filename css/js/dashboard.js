function renderTrafficChart(data) {
    const ctx = document.getElementById('trafficChart').getContext('2d');
    const hours = data.map(item => item.hour + ':00');
    const users = data.map(item => item.users);
    const pageViews = data.map(item => item.page_views);
    const orders = data.map(item => item.orders);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: hours,
            datasets: [
                {
                    label: 'Users',
                    data: users,
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Page Views',
                    data: pageViews,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Orders',
                    data: orders,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Traffic Patterns During Sale Event'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function renderSalesChart(data) {
    const ctx = document.getElementById('salesChart').getContext('2d');
    const categories = data.map(item => item.category);
    const sales = data.map(item => item.sales);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categories,
            datasets: [{
                label: 'Sales (₹)',
                data: sales,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)'
                ],
                borderColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)',
                    'rgb(255, 206, 86)',
                    'rgb(75, 192, 192)',
                    'rgb(153, 102, 255)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Sales by Category'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '₹' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

function simulateServerData() {
    const servers = ['server_1', 'server_2', 'server_3', 'server_4'];
    const data = [];
    
    for (let i = 0; i < 24; i++) {
        const hourData = {
            hour: i + ':00',
        };
        
        servers.forEach(server => {
            // Simulate load with peaks during business hours
            let load = 200;
            if (i >= 10 && i <= 20) {
                load = 600 + Math.random() * 400;
            } else if (i >= 8 && i <= 22) {
                load = 400 + Math.random() * 300;
            } else {
                load = 200 + Math.random() * 200;
            }
            
            hourData[server] = Math.round(load);
        });
        
        data.push(hourData);
    }
    
    return data;
}

function renderServerChart(data) {
    const ctx = document.getElementById('serverChart').getContext('2d');
    const hours = data.map(item => item.hour);
    const servers = ['server_1', 'server_2', 'server_3', 'server_4'];
    const colors = ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 206, 86)', 'rgb(75, 192, 192)'];
    
    const datasets = servers.map((server, index) => {
        return {
            label: server,
            data: data.map(item => item[server]),
            borderColor: colors[index],
            backgroundColor: colors[index].replace('rgb', 'rgba').replace(')', ', 0.1)'),
            fill: true,
            tension: 0.4
        };
    });
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: hours,
            datasets: datasets
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Server Load During Sale Event'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1000,
                    ticks: {
                        callback: function(value) {
                            return value + ' req/min';
                        }
                    }
                }
            }
        }
    });
}