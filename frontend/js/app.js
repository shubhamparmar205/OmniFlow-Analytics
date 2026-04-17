/* ==========================================================
   1. LIVE DIGITAL CLOCK
   ========================================================== */
function updateClock() {
    const clock = document.getElementById('digital-clock');
    const now = new Date();
    clock.innerText = now.toTimeString().split(' ')[0];
}
setInterval(updateClock, 1000);
updateClock();

const dateInput = document.getElementById('timestamp');
const now = new Date();
now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
dateInput.value = now.toISOString().slice(0, 16);

// Calendar icon native popup trigger
document.getElementById('calendar-icon-btn').addEventListener('click', () => {
    try {
        // Modern approach forcing the native HTML5 calendar block to open
        document.getElementById('timestamp').showPicker();
    } catch (e) {
        // Fallback for older browsers
        document.getElementById('timestamp').focus();
    }
});

// Auto-close calendar when the user finishes selecting the final parameter (minutes)
dateInput.addEventListener('change', function() {
    // Calling blur() forces the native browser popup to lose focus and safely dismiss itself
    this.blur();
});

/* ==========================================================
   2. INITIALIZE CHART.JS 24-HOUR FORECAST
   ========================================================== */
const ctx = document.getElementById('forecastChart').getContext('2d');
const gradientBlue = ctx.createLinearGradient(0, 0, 0, 400);
gradientBlue.addColorStop(0, 'rgba(0, 243, 255, 0.8)');
gradientBlue.addColorStop(1, 'rgba(0, 243, 255, 0)');

const historicalBaseline = [400, 350, 300, 280, 450, 800, 1500, 1800, 1600, 1300, 1200, 1250, 1300, 1350, 1400, 1500, 1900, 2100, 1800, 1400, 1100, 800, 600, 450];
const labels = Array.from({length: 24}, (_, i) => `${i}:00`);

const forecastChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [
            {
                label: 'Predicted Volume',
                data: [],
                borderColor: '#00f3ff',
                backgroundColor: gradientBlue,
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.4,
                fill: true
            },
            {
                label: 'Historical Baseline',
                data: historicalBaseline,
                borderColor: '#555',
                borderWidth: 2,
                borderDash: [5, 5],
                pointRadius: 0,
                tension: 0.4,
                fill: false
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { 
            legend: { 
                position: 'top',
                align: 'end',
                labels: { color: '#e0e5ff', font: { family: 'Share Tech Mono', size: 12 } } 
            },
            title: {
                display: true,
                text: 'AI SYNTHESIZED 24H CONGESTION METRICS',
                color: '#bc13fe',
                font: { size: 14, family: 'Inter', weight: '800', letterSpacing: 2 },
                padding: { top: 0, bottom: 15 }
            },
            tooltip: {
                backgroundColor: 'rgba(5, 5, 15, 0.9)',
                titleFont: { family: 'Share Tech Mono', size: 14 },
                bodyFont: { family: 'Share Tech Mono', size: 13 },
                borderColor: '#00f3ff',
                borderWidth: 1,
                callbacks: {
                    label: function(context) {
                        return context.dataset.label + ': ' + Math.round(context.raw) + ' Vehicles';
                    }
                }
            }
        },
        scales: {
            x: { 
                grid: { color: 'rgba(255,255,255,0.05)' }, 
                ticks: { color: '#7b84b5', font: { family: 'Share Tech Mono' } },
                title: { display: true, text: 'HOUR OF DAY (MILITARY TIME)', color: '#00f3ff', font: { family: 'Share Tech Mono', size: 11, letterSpacing: 1 } }
            },
            y: { 
                grid: { color: 'rgba(255,255,255,0.05)' }, 
                ticks: { color: '#7b84b5', font: { family: 'Share Tech Mono' } },
                title: { display: true, text: 'OBSERVED VEHICULAR VOLUME', color: '#00f3ff', font: { family: 'Share Tech Mono', size: 11, letterSpacing: 1 } },
                beginAtZero: true
            }
        }
    }
});

/* ==========================================================
   3. STATE MANAGEMENT & MICRO-INTERACTIONS
   ========================================================== */
document.getElementById('prediction-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const btn = document.getElementById('execute-btn');
    const cards = document.querySelectorAll('.skeleton-ready');
    const volumeBox = document.getElementById('volume-display');
    const deltaBox = document.getElementById('delta-display');

    cards.forEach(c => c.classList.remove('resolved'));
    btn.disabled = true;
    cards.forEach(c => c.classList.add('is-scanning'));
    
    const requestData = {
        timestamp: document.getElementById('timestamp').value + ":00",
        weather: document.getElementById('weather').value,
        events: document.getElementById('events').checked
    };

    const sequence = [
        "Initializing XGBoost Tensor...",
        "Interrogating AI Mathematical Weights...",
        "Generating Forecast..."
    ];
    
    for (let i = 0; i < sequence.length; i++) {
        setTimeout(() => { btn.textContent = sequence[i]; }, i * 600);
    }

    let serverData = null;
    let fetchError = false;

    try {
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });
        if (!response.ok) throw new Error("API Failure");
        serverData = await response.json();
    } catch (err) {
        fetchError = true;
        console.error(err);
    }

    setTimeout(() => {
        cards.forEach(c => c.classList.remove('is-scanning'));
        
        if (fetchError) {
            alert("Mission critical failure. Could not reach FastAPI Tensor on Port 8000.");
            btn.textContent = "Run Predictive Model";
            btn.disabled = false;
            return;
        }

        // 1. Reveal Final Output Strings in Card A
        volumeBox.textContent = serverData.predicted_volume;
        let diff = ((serverData.predicted_volume - serverData.base_volume) / serverData.base_volume) * 100;
        deltaBox.textContent = `${diff >= 0 ? '+' : ''}${diff.toFixed(1)}% vs Isolated Base`;
        deltaBox.style.color = diff > 0 ? '#ff2a2a' : '#00ff88';

        // 2. Render Chart.js Graph in Card B
        const simulatedDay = historicalBaseline.map(val => val * (serverData.predicted_volume / 1500));
        forecastChart.data.datasets[0].data = simulatedDay;
        forecastChart.update();

        // 3. Process Card C: AI Decision Impact Breakdown
        document.getElementById('base-vol').textContent = serverData.base_volume;
        
        const wVal = document.getElementById('weather-val');
        wVal.textContent = (serverData.weather_impact > 0 ? `+${serverData.weather_impact}` : serverData.weather_impact);
        wVal.className = 'impact-val ' + (serverData.weather_impact >= 0 ? 'highlight-danger' : 'highlight-positive');
        
        const eVal = document.getElementById('event-val');
        eVal.textContent = (serverData.event_impact > 0 ? `+${serverData.event_impact}` : serverData.event_impact);
        eVal.className = 'impact-val ' + (serverData.event_impact > 0 ? 'highlight-danger' : 'highlight-neutral');

        document.getElementById('total-val').textContent = serverData.predicted_volume;

        // Resolve States
        cards.forEach(c => c.classList.add('resolved'));
        
        btn.textContent = "Run Predictive Model";
        btn.disabled = false;

    }, 2000); 
});

/* ==========================================================
   5. TELEMETRY LATENCY MOCK (FOOTER)
   ========================================================== */
const latencyDisplay = document.getElementById('telemetry-latency');
setInterval(() => {
    // Generate random payload ms between 15 and 40
    const mockMs = Math.floor(Math.random() * (40 - 15 + 1)) + 15;
    latencyDisplay.textContent = mockMs + 'ms';
}, 2000);
