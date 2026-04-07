import streamlit as st
import streamlit.components.v1 as components

# 1. إعدادات الصفحة (يجب أن تكون أول أمر في بايثون)
st.set_page_config(
    page_title="ICU Riyadh | Modern Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. تعريف كود الـ HTML داخل متغير نصي واحد مغلق بدقة
dashboard_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #0a0e17;
            --glass: rgba(30, 41, 59, 0.7);
            --neon-blue: #38bdf8;
            --neon-red: #fb7185;
            --text: #f1f5f9;
        }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 20px;
            overflow-x: hidden;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 40px;
            background: var(--glass);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 25px;
        }
        .q-badge {
            background: var(--neon-blue);
            color: #0a0e17;
            padding: 10px 30px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 1.4rem;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 25px;
        }
        .card {
            background: var(--glass);
            backdrop-filter: blur(10px);
            border-radius: 25px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: 0.3s;
        }
        .card:hover { transform: translateY(-5px); border-color: var(--neon-blue); }
        .circle {
            width: 100px; height: 100px; border-radius: 50%;
            border: 5px solid rgba(255, 255, 255, 0.1);
            margin: 0 auto 15px; display: flex;
            align-items: center; justify-content: center;
            font-size: 1.7rem; font-weight: 800;
        }
        .blue { border-color: var(--neon-blue); color: var(--neon-blue); text-shadow: 0 0 10px var(--neon-blue); }
        .red { border-color: var(--neon-red); color: var(--neon-red); text-shadow: 0 0 10px var(--neon-red); }
        .label { font-weight: bold; color: #94a3b8; }
        .chart-box {
            background: var(--glass);
            border-radius: 25px;
            padding: 25px;
            height: 300px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1 style="margin:0; color:var(--neon-blue)">Executive ICU Dashboard</h1>
            <p style="margin:5px 0 0 0; color:#64748b">SGH Riyadh - Performance Monitoring</p>
        </div>
        <div class="q-badge" id="qLabel">4Q 2023</div>
    </div>

    <div class="grid" id="kpiGrid"></div>

    <div class="chart-box">
        <canvas id="barChart"></canvas>
    </div>

    <script>
        const timeline = [
            { q: "4Q 2023", v: [0, 7.3, 1.3, 1.5, 0, 5.2, 67, 13], b: [0.04, 26, 1.3, 1, 0.4, 1.6, 83, 8] },
            { q: "1Q 2024", v: [0.2, 6.4, 1.2, 2.1, 0.7, 4.8, 83, 20], b: [0.09, 7.7, 2.6, 2.4, 0.9, 4.4, 70, 19] },
            { q: "2Q 2024", v: [0.0, 6.5, 1.5, 2.0, 0.6, 3.7, 82, 18], b: [0.2, 14, 2.4, 1, 0.5, 6.2, 71, 12] },
            { q: "3Q 2024", v: [0.2, 4.6, 1.2, 1.8, 0.4, 4.5, 83, 18], b: [0.3, 6.9, 2.6, 1, 1, 4.6, 68, 19] }
        ];
        const titles = ["سقوط", "HAPI", "Blood", "VAE", "CAUTI", "Turnover", "BSN", "Hours"];
        let idx = 0; let chart;

        function update() {
            const data = timeline[idx];
            document.getElementById('qLabel').innerText = data.q;
            const grid = document.getElementById('kpiGrid');
            grid.innerHTML = '';

            data.v.forEach((v, i) => {
                const isBad = (i < 6) ? (v > data.b[i]) : (v < data.b[i]);
                const cls = isBad ? 'red' : 'blue';
                grid.innerHTML += `<div class="card"><div class="circle ${cls}">${v}</div><div class="label">${titles[i]}</div></div>`;
            });

            if(!chart) {
                const ctx = document.getElementById('barChart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'bar',
                    data: { labels: titles, datasets: [{ data: data.v, backgroundColor: '#38bdf8', borderRadius: 10 }] },
                    options: { maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { grid: { color: '#1e293b' } } } }
                });
            } else {
                chart.data.datasets[0].data = data.v;
                chart.update();
            }
            idx = (idx + 1) % timeline.length;
        }
        update(); setInterval(update, 8000);
    </script>
</body>
</html>
"""

# 3. عرض المكون النهائي
components.html(dashboard_html, height=900, scrolling=False)
