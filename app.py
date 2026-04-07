<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>ICU Riyadh | Saudi German Hospital Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root { --bg: #0f172a; --card: #1e293b; --blue: #38bdf8; --red: #fb7185; --text: #f1f5f9; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: auto; }
        .header { display: flex; justify-content: space-between; align-items: center; padding: 20px; border-bottom: 1px solid #334155; margin-bottom: 20px; }
        .q-tag { background: var(--blue); color: var(--bg); padding: 5px 20px; border-radius: 20px; font-weight: bold; font-size: 1.2rem; }
        
        /* KPI Grid */
        .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .card { background: var(--card); border-radius: 20px; padding: 20px; text-align: center; border: 1px solid #334155; position: relative; }
        .circle-svg { transform: rotate(-90deg); width: 120px; height: 120px; }
        .circle-bg { fill: none; stroke: #334155; stroke-width: 10; }
        .circle-proc { fill: none; stroke-width: 10; stroke-linecap: round; transition: stroke-dashoffset 1s ease; stroke: var(--blue); }
        .val { position: absolute; top: 55px; left: 50%; transform: translateX(-50%); font-size: 1.5rem; font-weight: bold; }
        .label { margin-top: 10px; font-size: 0.9rem; color: #94a3b8; }
        
        .chart-box { background: var(--card); padding: 25px; border-radius: 20px; border: 1px solid #334155; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>🏥 أداء العناية المركزة - مستشفى السعودي الألماني</h1>
        <div class="q-tag" id="qLabel">4Q 2023</div>
    </div>

    <div class="kpi-grid" id="kpiContainer"></div>

    <div class="chart-box">
        <canvas id="barChart" height="100"></canvas>
    </div>
</div>

<script>
// البيانات من ملفك المرفق
const periods = [
    { name: "4Q 2023", vals: [0, 7.30, 1.38, 1.57, 0, 5.21, 67.19, 13], bms: [0.04, 26.67, 1.3, 1.06, 0.46, 1.6, 83.53, 7.99] },
    { name: "1Q 2024", vals: [0.24, 6.45, 1.28, 2.17, 0.70, 4.84, 82.99, 20.14], bms: [0.09, 7.77, 2.67, 2.42, 0.99, 4.49, 70.31, 19.09] },
    { name: "2Q 2024", vals: [0.06, 6.54, 1.56, 2.04, 0.67, 3.74, 82.74, 18.22], bms: [0.24, 14.29, 2.42, 0, 0.51, 6.25, 71.21, 12.54] },
    
