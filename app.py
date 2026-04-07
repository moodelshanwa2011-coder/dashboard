<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>ICU Riyadh | Performance Executive Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --primary: #38bdf8;
            --danger: #ef4444;
            --text: #f8fafc;
        }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 30px;
            overflow-x: hidden;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .q-indicator {
            background: var(--primary);
            color: var(--bg);
            padding: 8px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 1.2rem;
            box-shadow: 0 0 15px var(--primary);
        }
        .kpi-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
            margin-bottom: 40px;
        }
        .kpi-card {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 24px;
            padding: 25px;
            text-align: center;
            transition: all 0.4s ease;
        }
        .circle-box {
            position: relative;
            width: 140px;
            height: 140px;
            margin: 0 auto 15px;
        }
        .kpi-value {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 2rem;
            font-weight: 700;
        }
        .metric-label {
            font-size: 1.1rem;
            color: #94a3b8;
            margin-bottom: 5px;
        }
        .benchmark-label {
            font-size: 0.85rem;
            color: #64748b;
        }
        canvas#mainChart {
            background: var(--card-bg);
            border-radius: 24px;
            padding: 30px;
            max-height: 400px;
        }
        svg { transform: rotate(-90deg); }
        circle { fill: none; stroke-width: 10; stroke-linecap: round; transition: all 1s ease; }
        .bg-ring { stroke: rgba(255,255,255,0.05); }
        .progress-ring { stroke-dasharray: 377; stroke-dashoffset: 377; }
    </style>
</head>
<body>

<div class="header">
    <div>
        <h1 style="margin:0; font-size: 1.8rem;">لوحة مؤشرات أداء ICU - الرياض</h1>
        <p style="color: #64748b; margin-top:5px;">المستشفى السعودي الألماني - تحليل البيانات السنوية</p>
    </div>
    <div class="q-indicator" id="qTitle">4Q 2023</div>
</div>

<div class="kpi-container" id="kpiGrid"></div>

<div style="width: 100%;">
    <canvas id="mainChart"></canvas>
</div>

<script>
// البيانات الفعلية المستخرجة من مستندك
const timeline = [
    { q: "4Q 2023", vals: [0, 7.30, 1.38, 1.57, 0, 5.21, 67.19, 13], b
