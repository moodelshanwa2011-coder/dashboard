import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ICU Executive Performance",
    layout="wide",
    initial_sidebar_state="collapsed"
)

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #020617;
            --card-bg: rgba(30, 41, 59, 0.45);
            --neon-cyan: #06b6d4;
            --neon-rose: #f43f5e;
            --text-dim: #94a3b8;
            --border: rgba(255, 255, 255, 0.08);
        }
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg);
            color: #f8fafc;
            margin: 0;
            padding: 20px;
            overflow: hidden;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            padding: 15px 35px;
            border-radius: 16px;
            border: 1px solid var(--border);
            margin-bottom: 20px;
        }
        .q-badge {
            background: linear-gradient(135deg, #0891b2, #22d3ee);
            color: #020617;
            padding: 8px 24px;
            border-radius: 8px;
            font-weight: 800;
            font-size: 1.1rem;
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.3);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }
        .square-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            transition: 0.3s;
        }
        .square-card:hover { border-color: var(--neon-cyan); background: rgba(6, 182, 212, 0.05); }
        .val { font-size: 2rem; font-weight: 900; margin-bottom: 5px; }
        .safe { color: var(--neon-cyan); text-shadow: 0 0 15px rgba(6, 182, 212, 0.4); }
        .alert { color: var(--neon-rose); text-shadow: 0 0 15px rgba(244, 63, 94, 0.4); }
        .label { font-size: 0.85rem; font-weight: 600; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px; }

        /* منطقة الرسم البياني والدائرة الكبيرة */
        .analytics-row {
            display: grid;
            grid-template-columns: 2fr 1.2fr; /* البار تشارت يسار والدائرة يمين */
            gap: 20px;
            height: 300px;
        }
        .glass-panel {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid var(--border);
            position: relative;
        }
        .gauge-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        #safetyScore {
            font-size: 3.5rem;
            font-weight: 900;
            color: var(--neon-cyan);
            margin-top: -10px;
        }
        .gauge-label { font-size: 1rem; color: var(--text-dim); font-weight: bold; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1 style="margin:0; font-size:1.4rem; letter-spacing:1px;">ICU <span style="color:var(--neon-cyan)">EXECUTIVE</span> ANALYTICS</h1>
            <p style="margin:4px 0 0 0; color:var(--text-dim); font-size:0.8rem;">Saudi German Hospital | Riyadh Operations</p>
        </div>
        <div class="q-badge" id="qLabel">4Q 2023</div>
    </div>

    <div class="grid" id="kpiGrid"></div>

    <div class="analytics-row">
        <div class="glass-panel">
            <canvas id="barChart"></canvas>
        </div>
        <div class="glass-panel gauge-container">
            <div id="safetyScore">0%</div>
            <div class="gauge-label">OVERALL SAFETY COMPLIANCE</div>
            <div style="font-size: 0.7rem; color: #475569; margin-top: 15px;">Calculated vs. NHCI Benchmarks</div>
        </div>
    </div>

    <script>
        const timeline = [
            { q: "4Q 2023", v: [0, 7.3, 1.38, 1.57, 0, 5.21, 67.2, 13.0], b: [0.04, 26.6, 1.3, 1.0, 0.4, 1.6, 83.5, 8.0] },
            { q: "1Q 2024", v: [0.24, 6.45, 1.28, 2.17, 0.70, 4.84, 83.0, 20.1], b: [0.09, 7.7, 2.6, 2.4, 0.9, 4.4, 70.3, 19.1] },
            { q: "2Q 2024", v: [0.06, 6.54, 1.56, 2.04, 0.67, 3.74, 82.7, 18.2], b: [0.24, 14.2, 2.4, 1.0, 0.5, 6.2, 71.2, 12.5] },
            { q: "3Q 2024", v: [0.28, 4.60, 1.20, 1.89, 0.40, 4.51, 83.4, 18.3], b: [0.36, 6.9, 2.6, 1.0, 1.0, 4.6, 68.2, 19.2] },
            { q: "1Q 2025", v: [1.59, 4.17, 1.26, 1.91, 0.43, 1.43, 83.8, 18.2], b: [0.12, 4.9, 3.0, 6.6, 0.5, 3.9, 70.0, 19.8] }
        ];

        const labels = ["Falls", "HAPI", "CLABSI", "VAE", "CAUTI", "Turnover", "BSN Edu", "RN Hours"];
        let idx = 0; let chart;

        function update() {
            const data = timeline[idx];
            document.getElementById('qLabel').innerText = data.q;
            const grid = document.getElementById('kpiGrid');
            grid.innerHTML = '';

            let passCount = 0;

            data.v.forEach((v, i) => {
                const isBad = (i < 6) ? (v > data.b[i]) : (v < data.b[i]);
                const cls = isBad ? 'alert' : 'safe';
                if (!isBad) passCount++;
                
                grid.innerHTML += `
                    <div class="square-card">
                        <div class="val ${cls}">${v}</div>
                        <div class="label">${labels[i]}</div>
                    </div>`;
            });

            // تحديث نسبة الأمان (Safety Score)
            const score = Math.round((passCount / 8) * 100);
            document.getElementById('safetyScore').innerText = score + "%";
            document.getElementById('safetyScore').style.color = score >= 75 ? "#06b6d4" : "#f43f5e";

            if(!chart) {
                const ctx = document.getElementById('barChart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'bar',
                    data: { labels: labels, datasets: [{ data: data.v, backgroundColor: '#06b6d4', borderRadius: 4, barThickness: 20 }] },
                    options: { 
                        maintainAspectRatio: false, 
                        plugins: { legend: { display: false } },
                        scales: { 
                            y: { grid: { color: 'rgba(255,255,255,0.03)' }, ticks: { color: '#475569', font: { size: 10 } } },
                            x: { ticks: { color: '#94a3b8', font: { size: 10, weight: 'bold' } } }
                        }
                    }
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

components.html(dashboard_html, height=800, scrolling=False)
