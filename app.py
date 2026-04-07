<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>SGH Riyadh - ICU Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        :root { --bg: #0f172a; --card: #1e293b; --blue: #38bdf8; --red: #fb7185; --text: #f1f5f9; }
        body { font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; overflow: hidden; }
        .header { display: flex; justify-content: space-between; align-items: center; padding: 10px 30px; border-bottom: 1px solid #334155; }
        .q-badge { background: var(--blue); color: #000; padding: 10px 25px; border-radius: 12px; font-weight: bold; font-size: 1.5rem; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; padding: 20px; }
        .card { background: var(--card); border-radius: 20px; padding: 15px; position: relative; border: 1px solid #334155; text-align: center; }
        .circle-svg { transform: rotate(-90deg); width: 100px; height: 100px; }
        .circle-bg { fill: none; stroke: #334155; stroke-width: 8; }
        .circle-fill { fill: none; stroke-width: 10; stroke-linecap: round; transition: stroke-dashoffset 1s ease; }
        .val { position: absolute; top: 40px; left: 50%; transform: translateX(-50%); font-size: 1.4rem; font-weight: bold; }
        .label { margin-top: 10px; font-size: 0.9rem; font-weight: bold; color: #94a3b8; }
        .chart-container { background: var(--card); border-radius: 20px; margin: 0 20px; padding: 15px; height: 280px; }
    </style>
</head>
<body>

<div class="header">
    <h1>لوحة مؤشرات أداء ICU - الرياض</h1>
    <div class="q-badge" id="qText">4Q 2023</div>
</div>

<div class="grid" id="kpiGrid"></div>

<div class="chart-container">
    <canvas id="mainChart"></canvas>
</div>

<script>
// البيانات الفعلية من ملف PDF الخاص بك
const stats = [
    { name: "4Q 2023", v: [0, 7.3, 1.38, 1.57, 0, 5.21, 67.2, 13.0], b: [0.04, 26.7, 1.3, 1.06, 0.46, 1.6, 83.5, 8.0] },
    { name: "1Q 2024", v: [0.24, 6.45, 1.28, 2.17, 0.7, 4.84, 83.0, 20.1], b: [0.09, 7.7, 2.6, 2.4, 0.9, 4.4, 70.3, 19.1] },
    { name: "2Q 2024", v: [0.06, 6.5, 1.5, 2.0, 0.6, 3.7, 82.7, 18.2], b: [0.2, 14.3, 2.4, 1.0, 0.5, 6.2, 71.2, 12.5] },
    { name: "3Q 2024", v: [0.28, 4.6, 1.2, 1.8, 0.4, 4.5, 83.3, 18.3], b: [0.3, 6.9, 2.6, 1.0, 1.0, 4.6, 68.2, 19.2] },
    { name: "1Q 2025", v: [1.59, 4.1, 1.2, 1.9, 0.4, 1.4, 83.7, 18.2], b: [0.1, 4.9, 3.0, 6.6, 0.5, 3.9, 70.0, 19.8] }
];

const titles = ["السقوط", "الضغط HAPI", "عدوى الدم", "VAE تنفس", "CAUTI مسالك", "دوران العمل", "تعليم BSN", "ساعات RN"];
let current = 0;
let chart;

function render() {
    const d = stats[current];
    document.getElementById('qText').innerText = d.name;
    const grid = document.getElementById('kpiGrid');
    grid.innerHTML = '';

    d.v.forEach((v, i) => {
        const bm = d.b[i];
        // أول 6 مؤشرات: الزيادة سيئة (أحمر). آخر 2: النقص سيء (أحمر).
        const isBad = (i < 6) ? (v > bm) : (v < bm);
        const color = isBad ? '#fb7185' : '#38bdf8';
        const offset = 314 - (Math.min(v, bm*2) / (bm*2)) * 314;

        grid.innerHTML += `
            <div class="card">
                <svg class="circle-svg" viewBox="0 0 120 120">
                    <circle class="circle-bg" cx="60" cy="60" r="50"></circle>
                    <circle class="circle-fill" cx="60" cy="60" r="50" style="stroke:${color}; stroke-dasharray:314; stroke-dashoffset:${offset}"></circle>
                </svg>
                <div class="val" style="color:${color}">${v}</div>
                <div class="label">${titles[i]}</div>
            </div>`;
    });

    if(!chart) {
        chart = new Chart(document.getElementById('mainChart'), {
            type: 'bar',
            data: { labels: titles, datasets: [{ data: d.v, backgroundColor: '#38bdf8', borderRadius: 8 }] },
            options: { maintainAspectRatio: false, plugins: { legend: { display: false } } }
        });
    } else {
        chart.data.datasets[0].data = d.v;
        chart.data.datasets[0].backgroundColor = d.v.map((v, i) => (i < 6 ? v > d.b[i] : v < d.b[i]) ? '#fb7185' : '#38bdf8');
        chart.update();
    }
    current = (current + 1) % stats.length;
}

render();
setInterval(render, 10000); // تحديث كل 10 ثوانٍ
</script>
</body>
</html>
