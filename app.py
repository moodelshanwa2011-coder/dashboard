<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>ICU Performance Dashboard | Riyadh</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #0f172a;
            --card: #1e293b;
            --blue: #38bdf8;
            --red: #fb7185;
            --text: #f1f5f9;
        }
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .header {
            width: 95%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            border-bottom: 1px solid #334155;
            margin-bottom: 20px;
        }
        .q-badge {
            background: var(--blue);
            color: #000;
            padding: 10px 30px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 1.6rem;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        }
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            width: 95%;
            margin-bottom: 30px;
        }
        .card {
            background: var(--card);
            border-radius: 25px;
            padding: 20px;
            text-align: center;
            border: 1px solid #334155;
            position: relative;
            transition: 0.3s;
        }
        .circle-svg {
            transform: rotate(-90deg);
            width: 120px;
            height: 120px;
        }
        .circle-bg { fill: none; stroke: #334155; stroke-width: 8; }
        .circle-progress {
            fill: none;
            stroke-width: 10;
            stroke-linecap: round;
            transition: 1s ease-in-out;
            stroke-dasharray: 314;
        }
        .value-text {
            position: absolute;
            top: 55px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 1.6rem;
            font-weight: bold;
        }
        .label-text {
            margin-top: 15px;
            font-size: 1rem;
            font-weight: 600;
            color: #94a3b8;
        }
        .chart-box {
            width: 95%;
            background: var(--card);
            padding: 25px;
            border-radius: 25px;
            border: 1px solid #334155;
            height: 350px;
        }
    </style>
</head>
<body>

<div class="header">
    <h1>🏥 وحدة العناية المركزة - الرياض | مؤشرات KPI</h1>
    <div class="q-badge" id="quarterDisplay">4Q 2023</div>
</div>

<div class="kpi-grid" id="kpiContainer"></div>

<div class="chart-box">
    <canvas id="barChart"></canvas>
</div>

<script>
// البيانات المستخرجة بدقة من المستند المرفق (8 مؤشرات)
const dataPoints = [
    { name: "4Q 2023", v: [0, 7.3, 1.38, 1.57, 0, 5.21, 67.2, 13.0], b: [0.04, 26.7, 1.3, 1.0, 0.4, 1.6, 83.5, 8.0] },
    { name: "1Q 2024", v: [0.24, 6.45, 1.28, 2.17, 0.7, 4.84, 83.0, 20.1], b: [0.09, 7.7, 2.6, 2.4, 0.9, 4.4, 70.3, 19.1] },
    { name: "2Q 2024", v: [0.06, 6.54, 1.56, 2.04, 0.67, 3.74, 82.7, 18.2], b: [0.24, 14.3, 2.4, 1.0, 0.5, 6.2, 71.2, 12.5] },
    { name: "3Q 2024", v: [0.28, 4.60, 1.20, 1.89, 0.40, 4.51, 83.4, 18.3], b: [0.36, 6.9, 2.6, 1.0, 1.0, 4.6, 68.2, 19.2] },
    { name: "1Q 2025", v: [1.59, 4.17, 1.26, 1.91, 0.43, 1.43, 83.8, 18.2], b: [0.12, 4.9, 3.0, 6.6, 0.5, 3.9, 70.0, 19.8] }
];

const labels = ["السقوط", "الضغط HAPI", "عدوى الدم", "VAE تنفس", "CAUTI مسالك", "دوران العمل", "تعليم BSN", "ساعات RN"];
let idx = 0;
let chart;

function updateDashboard() {
    const current = dataPoints[idx];
    document.getElementById('quarterDisplay').innerText = current.name;
    const container = document.getElementById('kpiContainer');
    container.innerHTML = '';

    current.v.forEach((v, i) => {
        const bm = current.b[i];
        // قاعدة الألوان: أحمر إذا ساءت النتيجة (زيادة إصابات أو نقص تعليم)
        const isBad = (i < 6) ? (v > bm) : (v < bm);
        const color = isBad ? '#fb7185' : '#38bdf8';
        const offset = 314 - (Math.min(v, bm*2) / (bm*2)) * 314;

        container.innerHTML += `
            <div class="card">
                <svg class="circle-svg" viewBox="0 0 120 120">
                    <circle class="circle-bg" cx="60" cy="60" r="50"></circle>
                    <circle class="circle-progress" cx="60" cy="60" r="50" style="stroke:${color}; stroke-dashoffset:${offset}"></circle>
                </svg>
                <div class="value-text" style="color:${color}">${v}</div>
                <div class="label-text">${labels[i]}</div>
                <div style="font-size:0.7rem; color:#64748b">Benchmark: ${bm}</div>
            </div>`;
    });

    if(!chart) {
        const ctx = document.getElementById('barChart').getContext('2d');
        chart = new Chart(ctx, {
            type: 'bar',
            data: { labels: labels, datasets: [{ data: current.v, backgroundColor: '#38bdf8', borderRadius: 10 }] },
            options: { maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { grid: { color: '#334155' } } } }
        });
    } else {
        chart.data.datasets[0].data = current.v;
        chart.data.datasets[0].backgroundColor = current.v.map((v, i) => (i < 6 ? v > current.b[i] : v < current.b[i]) ? '#fb7185' : '#38bdf8');
        chart.update();
    }
    idx = (idx + 1) % dataPoints.length;
}

updateDashboard();
setInterval(updateDashboard, 10000); // التغيير كل 10 ثوانٍ
</script>
</body>
</html>
