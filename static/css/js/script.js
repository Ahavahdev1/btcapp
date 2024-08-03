document.getElementById('purchaseForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const value = document.getElementById('value').value;

    fetch('/buy', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ value }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('btcAmount').textContent = `Purchased BTC: ${data.amount_btc.toFixed(6)}`;
        document.getElementById('totalBTC').textContent = `Total BTC: ${data.total_btc.toFixed(6)}`;
        document.getElementById('profitLoss').textContent = `Profit/Loss: $${data.profit_loss.toFixed(2)}`;
        document.getElementById('profitLossPercentage').textContent = `Profit/Loss Percentage: ${data.profit_loss_percentage.toFixed(2)}%`;
        
        // Fetch the purchases and plot the chart
        fetchPurchases();
    })
    .catch(error => console.error('Error:', error));
});

function fetchPurchases() {
    fetch('/purchases')
    .then(response => response.json())
    .then(data => {
        plotChart(data);
    });
}

function plotChart(purchases) {
    const ctx = document.getElementById('purchaseChart').getContext('2d');
    const dates = purchases.map(p => p.created_on);
    const values = purchases.map(p => p.fields['Value']);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Bitcoin Purchases',
                data: values,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}
