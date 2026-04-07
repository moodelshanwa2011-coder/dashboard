<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Executive ICU Dashboard - Riyadh</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root { --bg: #0f172a; --card: #1e293b; --blue: #38bdf8; --red: #fb7185; --text: #f1f5f9; }
        body { font-family: sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; text-align: center; }
        .header { display: flex; justify-content: space-between; align-items: center; padding: 10px 40px; border-bottom: 1px solid #334155; }
        .q-tag { background: var(--blue); color: #000; padding: 10px 20px; border-radius: 12px; font-weight: bold; font-size: 1.4rem; box-shadow: 0 0 15px var(--blue); }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; padding: 20px; }
        .card { background: var(--card); border-radius: 20px; padding: 20px; position: relative; border: 1px solid #334155; }
        .circle-svg { transform: rotate(-90deg); width: 120px; height: 120px; }
        .circle-bg { fill: none; stroke: #334155; stroke-width: 8; }
        .circle-fill { fill: none; stroke-width: 10; stroke-linecap: round; transition: stroke-dashoffset 1s ease; }
        .val { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 1.6rem; font-weight: bold; margin-top: -10px; }
        .label { margin-top: 15px; font-weight: bold; color: #94a3b8; }
        .chart-box { background: var(--card); border-radius: 20px; margin: 20px; padding: 20px; height: 350px; }
    </style>
</head>
<body>

<div class="header">
    <h1>لوحة أداء العناية المركزة - الرياض</h1>
    <div class="q-tag" id="qLabel">4Q 2023</div>
</div>

<div class="grid" id="kpiGrid"></div>

<div class="chart-box">
    <canvas id="barChart"></canvas>
</div>

<script>
// البيانات الفعلية المختصرة لـ 8 مؤشرات
const data = [
    { name: "4Q 2023", v: [0, 7.3, 1.38, 1.57, 0, 5.21, 67.2, 13], b: [0.04, 26.7, 1.3, 1.06, 0.46, 1.6, 83.5, 8.0] },
    { name: "1Q 2024", v: [0.24, 6.45, 1.28, 2.17, 0.7, 4.84, 83.0, 20.1], b: [0.09, 7.77, 2.67, 2.42, 0.99, 4.49, 70.3, 19.1] },
    { name: "2Q 2024", v: [0.06, 6.54, 1.56, 2.04, 0.67, 3.74, 82.7, 18.2], b: [0.24, 14.3, 2.42, 1.0, 0.51, 6.25, 71.2, 12.5] },
    { name: "3Q 2024", v: [0.28, 4.60, 1.20, 1.89, 0.40, 4.51, 83.4, 18.3], b: [0.36, 6.9, 2.63, 1.0, 1.02, 4.69, 68.3, 19.2] },
    { name: "1Q 2025", v: [1.59, 4.17, 1.26, 1.91, 0.43, 1.43, 83.8, 18.3], b: [0.12, 4.96, 3.02, 6.69, 0.5, 3.97, 70.0, 19.8] }
];

const labels = ["سقوط المرضى", "إصابات الضغط", "عدوى الدم", "VAE تنفس", "CAUTI مسالك", "دوران العمل", "تعليم BSN", "ساعات RN"];
let idx = 0;
let myChart;

function update() {
    const current = data[idx];
    document.getElementById('qLabel').innerText = current.name;
    const grid = document.getElementById('kpiGrid');
    grid.innerHTML = '';

    current.v.forEach((v, i) => {
        const bm = current.b[i];
        // تحديد اللون: أحمر لو تجاوز المرجع في أول 6 مؤشرات
        const isBad = (i < 6) ? (v > bm) : (v < bm
