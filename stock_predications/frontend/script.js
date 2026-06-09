const API_BASE = 'http://127.0.0.1:8000/api';

const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const autocompleteList = document.getElementById('autocompleteList');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('results');
const errorMsg = document.getElementById('errorMsg');

let companies = [];
let chartInstance = null;

// Fetch companies for autocomplete on load
async function fetchCompanies() {
    try {
        const response = await fetch(`${API_BASE}/companies`);
        if (response.ok) {
            companies = await response.json();
            console.log("Cached companies length:", companies.length);
        }
    } catch (err) {
        console.error('Failed to fetch companies list', err);
    }
}

fetchCompanies();

// Autocomplete Logic
searchInput.addEventListener('input', function() {
    const val = this.value;
    autocompleteList.innerHTML = '';
    
    if (!val) {
        autocompleteList.style.display = 'none';
        return;
    }
    
    const matches = companies.filter(c => c.toLowerCase().includes(val.toLowerCase())).slice(0, 5);
    
    if (matches.length > 0) {
        autocompleteList.style.display = 'block';
        matches.forEach(match => {
            const div = document.createElement('div');
            div.className = 'autocomplete-item';
            div.innerHTML = `<strong>${match.substr(0, val.length)}</strong>${match.substr(val.length)}`;
            div.addEventListener('click', function() {
                searchInput.value = match;
                autocompleteList.style.display = 'none';
                searchPrediction();
            });
            autocompleteList.appendChild(div);
        });
    } else {
        autocompleteList.style.display = 'none';
    }
});

// Close autocomplete if clicked outside
document.addEventListener('click', e => {
    if (e.target !== searchInput) {
        autocompleteList.style.display = 'none';
    }
});

searchBtn.addEventListener('click', searchPrediction);
searchInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
        autocompleteList.style.display = 'none';
        searchPrediction();
    }
});

async function searchPrediction() {
    const ticker = searchInput.value.trim();
    if (!ticker) return;

    // Reset UI
    resultsSection.classList.add('hidden');
    errorMsg.classList.add('hidden');
    loading.classList.remove('hidden');

    try {
        const response = await fetch(`${API_BASE}/prediction/${encodeURIComponent(ticker)}`);
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Prediction data not found');
        }

        const data = await response.json();
        renderPrediction(data);
    } catch (err) {
        showError(err.message);
    } finally {
        loading.classList.add('hidden');
    }
}

function renderPrediction(data) {
    const { next_day, forecast_30_days } = data;
    
    // Update Next Day Card
    document.getElementById('predictionDate').textContent = `Target Date: ${next_day.prediction_date}`;
    document.getElementById('currentPrice').textContent = `₹${next_day.current_price.toFixed(2)}`;
    document.getElementById('predictedPrice').textContent = `₹${next_day.predicted_next_day_price.toFixed(2)}`;
    
    const directionBadge = document.getElementById('directionBadge');
    const directionIcon = document.getElementById('directionIcon');
    const changePct = document.getElementById('changePercent');
    
    // Direction logic
    if (next_day.direction.includes('UP') || next_day.change_percent > 0) {
        directionBadge.className = 'direction-badge up';
        directionIcon.innerHTML = '📈 UP';
        changePct.textContent = `+${Math.abs(next_day.change_percent)}%`;
    } else {
        directionBadge.className = 'direction-badge down';
        directionIcon.innerHTML = '📉 DOWN';
        changePct.textContent = `-${Math.abs(next_day.change_percent)}%`;
    }

    // Chart Logic
    const chartContainer = document.getElementById('chartContainer');
    if (forecast_30_days && forecast_30_days.length > 0) {
        chartContainer.classList.remove('hidden');
        renderChart(ticker=next_day.company, forecast_30_days);
    } else {
        chartContainer.classList.add('hidden');
    }

    resultsSection.classList.remove('hidden');
}

function renderChart(ticker, forecastData) {
    const ctx = document.getElementById('forecastChart').getContext('2d');
    
    // Destroy previous instance
    if (chartInstance) {
        chartInstance.destroy();
    }

    const labels = forecastData.map(d => {
        const date = new Date(d.date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });
    
    const dataPoints = forecastData.map(d => d.predicted_close);

    // Gradient logic
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(139, 92, 246, 0.5)'); // primary color transparent
    gradient.addColorStop(1, 'rgba(139, 92, 246, 0.0)');

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `30-Day Forecast (${ticker})`,
                data: dataPoints,
                borderColor: '#8b5cf6', // primary color
                backgroundColor: gradient,
                borderWidth: 3,
                pointBackgroundColor: '#3b82f6', // accent color
                pointBorderColor: '#fff',
                pointRadius: 4,
                pointHoverRadius: 6,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#f8fafc' } // text-main
                },
                tooltip: {
                    backgroundColor: 'rgba(30, 41, 59, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    padding: 10,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return `₹${context.parsed.y.toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255,255,255,0.05)', drawBorder: false },
                    ticks: { color: '#94a3b8' } // text-muted
                },
                y: {
                    grid: { color: 'rgba(255,255,255,0.05)', drawBorder: false },
                    ticks: { color: '#94a3b8' } // text-muted
                }
            }
        }
    });
}

function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.classList.remove('hidden');
}
