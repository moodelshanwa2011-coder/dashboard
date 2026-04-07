<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>ICU Dashboard - SGH Riyadh</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Arial', sans-serif; background-color: #f8fafc; color: #1e293b; margin: 0; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; border-bottom: 3px solid #007bff; padding-bottom: 10px; }
        .q-label { font-size: 2rem; font-weight: bold; color: #007bff; background: white; padding: 10px 30px; border-radius: 50px; shadow: 0 4px 6px rgba(0,0,0,0.1); }
        
        /* تصميم الـ 8 دوائر */
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; padding: 20px; }
        .kpi-card { background: white; border-radius: 20px; padding: 20px; text-align: center; box-shadow: 0 10px 15px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }
        .circle { width: 120px; height: 120px; border-radius: 50%; border: 10px solid #edf2f7; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: 800; transition: all 0.6s ease; }
        
        /* حالات الألوان */
        .safe { border-color: #007bff; color: #007bff; }
        .danger { border-color: #ef4444; color: #ef4444; }
        
        .label { font-size: 1.1rem; font-weight: 600; color: #64748b; }
        .chart-box { width: 90%; margin: 40px auto; background: white; padding: 20px; border-radius: 20px; box-shadow: 0 10px 15px rgba(0,0,0,0.05); }
    </style>
</head>
<body>

<div class="header">
    <h1>لوحة مؤشرات أداء العناية المركزة - الرياض</h1>
    <span class="q-label" id="currentQ">4Q 2023</span>
</div>

<div class="grid" id="kpiGrid"></div>

<div class="chart-box">
    <canvas id="barChart" height="100"></canvas>
</div>

<script>
// البيانات الفعلية المستخرجة من جدولك
const data = [
    { q: "4Q 2023", v: [0, 7.30, 1.38, 1.57, 0, 5.21, 67.19, 13.0], b: [0.04, 26.67, 1.3, 1.06, 0.46, 1.6, 83.53, 7.99] },
    { q: "1Q 2024", v: [0.24, 6.45, 1.28, 2.17, 0.70, 4.84, 82.99, 20.14], b: [0.09, 7.77, 2.67, 2.42, 0.99, 4.49, 70.31, 19.09] },
    { q: "2Q 2024", v: [0.06, 6.54, 1.56, 2.04, 0.67, 3.74, 82.74, 18.22], b: [0.24, 14.29, 2.42, 1.0, 0.51, 6.25, 71.21, 12.54] },
    { q: "3Q 2024", v: [0.28, 4.60, 1.20, 1.89, 0.40, 4.51, 83.36, 18.34], b: [0.36, 6.9, 2.63, 1.0, 1.02, 4.69, 68.25, 19.20] },
    { q: "1Q 2025", v: [1.59, 4.17, 1.26, 1.91, 0.43, 1.43, 83.78, 18.28], b: [0.12, 4.96, 3.02, 6.69, 0.5, 3.97, 70.0, 19.82] }
];

const labels = ["سقوط المرضى", "إصابات الضغط", "عدوى الدم", "VAE تنفس", "CAUTI مسالك", "دوران العمل", "تعليم
