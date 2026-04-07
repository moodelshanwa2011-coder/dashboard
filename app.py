<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>ICU Riyadh Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background-color: #0f172a; color: white; font-family: sans-serif; text-align: center; margin: 0; padding: 20px; }
        .header { border-bottom: 2px solid #1e293b; padding-bottom: 10px; margin-bottom: 20px; }
        .q-title { font-size: 24px; color: #38bdf8; background: #1e293b; display: inline-block; padding: 10px 20px; border-radius: 10px; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; padding: 10px; }
        .card { background: #1e293b; border-radius: 15px; padding: 15px; border: 1px solid #334155; position: relative; }
        .circle { width: 100px; height: 100px; border: 8px solid #334155; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: bold; transition: 0.5s; }
        .blue { border-color: #38bdf8; color: #38bdf8; }
        .red { border-color: #fb7185; color: #fb7185; }
        .label { margin-top: 10px; font-size: 14px; color: #94a3b8; }
        .chart-container { width: 90%; height: 300px; margin: 30px auto; background: #1e293b; padding: 20px; border-radius: 15px; }
    </style>
</head>
<body>

<div class="header">
    <h1>لوحة أداء العناية المركزة - الرياض</h1>
    <div class="q-title" id="qLabel">4Q 2023</div>
</div>

<div class="grid" id="kpiGrid"></div>

<div class="chart-container">
    <canvas id="barChart"></canvas>
</div>

<script>
// البيانات من جدولك (8 مؤشرات عبر 5 فترات زمنية)
const timeline = [
    { q: "4Q 2023", v: [0, 7.3, 1.3, 1.5, 0, 5.2, 67, 13], b: [0.04, 26, 1.3, 1.0, 0.4, 1.6, 83, 8.0] },
    { q: "1Q 2024", v: [0.2, 6.4, 1.2, 2.1, 0.7, 4.8, 83, 20], b: [0.09, 7.7, 2.6, 2.4, 0.9, 4.4, 70, 19] },
    { q: "2Q 2024", v: [0.0, 6.5, 1.5, 2.0, 0.6, 3.7, 82, 18], b: [0.2, 14, 2.4, 1.0, 0.5, 6.2, 71, 12] },
    { q: "3Q 2024", v: [0.2, 4.6, 1.2, 1.8, 0.4, 4.5, 83, 18], b: [0.3, 6.9, 2.6, 1.0, 1.0, 4.6, 68, 19] },
    { q: "1Q 2025", v: [1.5, 4.1, 1.2, 1.9, 0.4, 1.4, 83, 18], b: [0.1, 4.9, 3.0, 6.6, 0.5, 3.9, 70, 19] }
];

const labels = ["سقوط", "HAPI", "CLABSI", "VAE", "CAUTI", "Turnover", "BSN", "Hours"];
let idx = 0;
let chart;

function update() {
    const data = timeline[idx];
    document.getElementById('qLabel').innerText = data.q;
    const grid = document.getElementById('kpiGrid');
    grid.innerHTML = '';

    data.v.forEach((v, i) => {
        const bm = data.b[i];
        // أول 6 مؤشرات: لو القيمة أكبر من المرجع = أحمر. آخر 2: لو أقل = أحمر.
        const isBad = (i < 6) ? (v > bm) : (v < bm);
        const colorClass = isBad ? 'red' : 'blue';

        grid.innerHTML += `
            <div class="card">
                <div class="circle ${colorClass}">${v}</div>
                <div class="label">${labels[i]}</div>
                <div style="font-size:10px; color:#64748b">BM: ${bm}</div>
            </div>`;
    });

    if(!chart) {
        chart = new Chart(document.getElementById('barChart'), {
            type: 'bar',
            data: { labels: labels, datasets: [{ data: data.v, backgroundColor: '#38bdf8' }] },
            options: { maintainAspectRatio: false, plugins: { legend: { display: false } } }
        });
    } else {
        chart.data.datasets[0].data = data.v;
        chart.update();
    }
    idx = (idx + 1) % timeline.length;
}

update();
setInterval(update, 10000); // تحديث كل 10 ثوانٍ
</script>
</body>
</html>
