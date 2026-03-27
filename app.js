// TAB SWITCHING LOGIC
function switchTab(tabId, targetBtn) {
    document.querySelectorAll('.page-section').forEach(page => {
        page.classList.add('hidden');
    });
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    document.getElementById(tabId).classList.remove('hidden');
    targetBtn.classList.add('active');
}

// Chart.js Configuration
const ctx = document.getElementById('trafficChart').getContext('2d');

Chart.defaults.color = '#8b9bb4';
Chart.defaults.font.family = 'Rajdhani';

const trafficChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Packet Count / sec',
                data: [],
                borderColor: '#00f0ff',
                backgroundColor: 'rgba(0, 240, 255, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                yAxisID: 'y'
            },
            {
                label: 'Entropy',
                data: [],
                borderColor: '#ff3366',
                backgroundColor: 'transparent',
                borderWidth: 2,
                borderDash: [5, 5],
                tension: 0.4,
                yAxisID: 'y1'
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: 'top' },
            tooltip: { mode: 'index', intersect: false }
        },
        scales: {
            x: {
                grid: { color: 'rgba(100, 150, 255, 0.1)' }
            },
            y: {
                type: 'linear',
                display: true,
                position: 'left',
                grid: { color: 'rgba(100, 150, 255, 0.1)' }
            },
            y1: {
                type: 'linear',
                display: true,
                position: 'right',
                grid: { drawOnChartArea: false },
                min: 0,
                max: 10
            }
        }
    }
});

let lastPacketId = null;

// FETCH DATA FROM BACKEND
async function fetchTrafficData() {
    try {
        const response = await fetch('/api/results');
        const json = await response.json();

        if (json.data && json.data.length > 0) {
            updateDashboard(json.data);
        }
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// UPDATE DASHBOARD
function updateDashboard(data) {
    const latest = data[0];

    if (latest.id === lastPacketId) return;
    lastPacketId = latest.id;

    document.getElementById('metric-count').innerText = latest.packet_count.toLocaleString();
    document.getElementById('metric-size').innerText = latest.packet_size.toLocaleString();
    document.getElementById('metric-entropy').innerText = latest.entropy.toFixed(2);

    const threatEl = document.getElementById('metric-threat');
    const globalStatus = document.getElementById('global-status');
    const pulseDot = document.querySelector('.pulse-dot');

    if (latest.status === 'MALICIOUS') {
        threatEl.innerText = 'DDoS THREAT!';
        threatEl.className = 'text-danger';
        globalStatus.innerText = 'ATTACK DETECTED - ACTIVE MITIGATION';
        globalStatus.className = 'status-value danger';

        pulseDot.style.backgroundColor = 'var(--red)';
        pulseDot.style.boxShadow = '0 0 15px var(--red)';
    } else {
        threatEl.innerText = 'NORMAL';
        threatEl.className = 'text-safe';
        globalStatus.innerText = 'ACTIVE (NETWORK DIAGNOSTICS)';
        globalStatus.className = 'status-value safe';

        pulseDot.style.backgroundColor = 'var(--cyan)';
        pulseDot.style.boxShadow = '0 0 15px var(--cyan)';
    }

    const times = data.map(d => d.timestamp).reverse();
    const counts = data.map(d => d.packet_count).reverse();
    const entropies = data.map(d => d.entropy).reverse();

    trafficChart.data.labels = times;
    trafficChart.data.datasets[0].data = counts;
    trafficChart.data.datasets[1].data = entropies;
    trafficChart.update();

    const logContainer = document.getElementById('ai-log');
    const isDanger = latest.status === 'MALICIOUS';

    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${isDanger ? 'danger' : ''}`;
    logEntry.innerHTML = `
        <div class="log-meta">
            <span>[${latest.timestamp}] PKT</span>
            <span class="badge ${isDanger ? 'danger' : 'safe'}">${latest.status}</span>
        </div>
        <div class="log-reason">${latest.reason}</div>
    `;

    logContainer.insertBefore(logEntry, logContainer.firstChild);

    if (logContainer.children.length > 50) {
        logContainer.removeChild(logContainer.lastChild);
    }
}

// RUN LIVE FETCH
fetchTrafficData();
setInterval(fetchTrafficData, 1000);

// SLIDESHOW
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const totalSlides = slides.length;
const indicator = document.getElementById('slide-indicator');

function updateSlide() {
    slides.forEach((slide, index) => {
        if (index === currentSlide) slide.classList.add('slide-active');
        else slide.classList.remove('slide-active');
    });
    indicator.innerText = `${currentSlide + 1} / ${totalSlides}`;
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    updateSlide();
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    updateSlide();
}

// MODAL LOGIC
const modalOverlay = document.getElementById('ai-modal');
const modalStatus = document.getElementById('modal-status');
const modalReason = document.getElementById('modal-reason');

function closeModal() {
    modalOverlay.classList.add('hidden');
}

// MANUAL TEST FORM
document.getElementById('manual-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const count = document.getElementById('manual-count').value;
    const size = document.getElementById('manual-size').value;
    const entropy = document.getElementById('manual-entropy').value;

    modalOverlay.classList.remove('hidden');
    modalStatus.innerText = 'CONNECTING TO AI ENGINE...';
    modalReason.innerHTML = '<div style="text-align:center; padding: 40px;">Processing...</div>';

    try {
        const response = await fetch('/api/manual', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                packet_count: parseInt(count),
                packet_size: parseInt(size),
                entropy: parseFloat(entropy)
            })
        });

        const data = await response.json();

        if (data.status.includes('MALICIOUS')) {
            modalStatus.style.color = 'var(--red)';
            modalStatus.innerText = '⚠️ ' + data.status;
        } else {
            modalStatus.style.color = 'var(--cyan)';
            modalStatus.innerText = '✅ ' + data.status;
        }

        modalReason.innerHTML = data.detailed_explanation;

    } catch (err) {
        console.error(err);
        modalStatus.innerText = 'SYSTEM ERROR';
        modalReason.innerHTML = 'Failed to connect to server.';
    }
});
