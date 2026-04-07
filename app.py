<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>ICU Dashboard - SGH Riyadh</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f0f4f8; color: #2d3748; margin: 0; padding: 20px; }
        .header { text-align: center; padding: 20px; background: #fff; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 30px; border-top: 5px solid #0056b3; }
        h1 { margin: 0; color: #0056b3; }
        .q-tag { display: inline-block; margin-top: 10px; padding: 8px 25px; background: #0056b3; color: #fff; border-radius: 50px; font-weight: bold; font-size: 1.4rem; }
        
        /* شبكة المؤشرات الـ 8 */
        .kpi-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; max-width: 1200px; margin: 0 auto; }
        .card { background: #fff; border-radius: 20px; padding: 25px; text-align: center; box-shadow: 0 10px 15px rgba(0,0,0,0.05); transition: transform 0.3s; }
        .card:hover { transform: translateY(-5px); }
        
        /* الدائرة الرقمية */
        .circle { width: 110px; height: 110px; border-radius: 50%; border: 8px solid #e2e8f0; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: bold; }
        .blue-status { border-color: #007bff; color: #007bff; }
        .red-status { border-color: #e53e3e; color: #e53e3e; }
        
        .title { font-weight: bold; font-size: 1.1rem; color: #4a5568; }
        .bm-text { font-size: 0.85rem; color: #a0aec0; margin-top: 5px; }
        
        /* منطقة البار تشارت */
        .chart-section { max-width: 1200px; margin: 40px auto; background: #fff; padding: 25px; border-radius: 20px; box-shadow: 0 10px 15px rgba(0,0,0,0.05); }
    </style>
</head>
<body>

<div class="header">
    <h1>لوحة مؤشرات أداء العناية المركزة - الرياض</h1>
    <div class="q-tag" id="periodName">4Q 2023</div>
</div>

<div class="kpi-container" id="kpiGrid"></div>

<div class="chart-section">
    <canvas id="mainBarChart" height="100"></canvas>
</div>

<script>
// البيانات المختصرة والدقيقة (8 مؤشرات)
const allData = [
    { label: "4Q 2023", values: [0, 7.30, 1.38, 1.57, 0, 5.21, 67.2, 13.0], bm: [0.04, 26.6, 1.3, 1.0, 0.4, 1.6, 83.5, 8.0] },
    { label: "1Q 2024", values: [0.24, 6.45, 1.28, 2.17, 0.70, 4.84, 83.0, 20.1], bm: [0.09, 7.7, 2.6, 2.4, 0.9, 4.4, 70.3, 19.1] },
    { label: "2Q 2024", values: [0.06, 6.54, 1.56, 2.04, 0.67, 3.74, 82.7, 18.2], bm: [0.24, 14.2, 2.4, 1.0, 0.5, 6.2, 71.2, 12.5] },
    { label: "3Q 2024", values: [0.28, 4.60, 1.20, 1.89, 0.40, 4.51, 83.4, 18.3], bm: [0.36, 6.9, 2.6, 1.0, 1.0, 4.6, 68.2, 19.2] },
    { label: "1Q 2025", values: [1.59, 4.17, 1.26, 1.91, 0.43, 1.43, 83.8, 18.2], bm: [0.12, 4.9, 3.0, 6.6, 0.5, 3.9, 70.0, 19.8] }
];

const kpiTitles = ["السقوط", "إصابات الضغط", "عدوى الدم", "VAE تنفس", "CAUTI مسالك", "دوران العمل", "تعليم BSN", "ساعات RN"];
let stepIdx = 0;
let chart;

function render() {
    const current = allData[stepIdx];
    document.getElementById('periodName').innerText = current.label;
    const grid = document.getElementById('kpiGrid');
    grid.innerHTML = '';

    current.values.forEach((val, i) => {
        const benchmark = current.bm[i];
        // المنطق اللوني: أول 6 سيئة إذا زادت، آخر 2 سيئة إذا نقصت
        const isWarning = (i < 6) ? (val > benchmark) : (val < benchmark);
        const colorClass = isWarning ? 'red-status' : 'blue-status';

        grid.innerHTML += `
            <div class="card">
                <div class="circle ${colorClass}">${val}</div>
                <div class="title">${kpiTitles[i]}</div>
                <div class="bm-text">المرجع: ${benchmark}</div>
            </div>`;
    });

    // تحديث البار تشارت
    if(!chart) {
        const ctx = document.getElementById('mainBarChart').getContext('2d');
        chart = new Chart(ctx, {
            type: 'bar',
            data: { 
                labels: kpiTitles, 
                datasets: [{ data: current.values, backgroundColor: '#007bff', borderRadius: 8 }] 
            },
            options: { responsive: true, plugins: { legend: { display: false } } }
        });
    } else {
        chart.data.datasets[0].data = current.values;
        chart.data.datasets[0].backgroundColor = current.values.map((v, i) => 
            (i < 6 ? v > current.bm[i] : v < current.bm[i]) ? '#e53e3e' : '#007bff'
        );
        chart.update();
    }

    stepIdx = (stepIdx + 1) % allData.length;
}

render();
setInterval(render, 10000); // تحديث كل 10 ثوانٍ
</script>
</body>
</html>
