import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(
    page_title="3FGW Dammam Dashboard",
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
            --card-bg: rgba(15, 23, 42, 0.8);
            --neon-blue: #22d3ee;
            --neon-red: #f43f5e;
            --border-clr: rgba(255, 255, 255, 0.1);
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
        }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0; padding: 25px; overflow: hidden;
        }
        .dashboard-container { max-width: 1580px; margin: 0 auto; }
        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--card-bg); backdrop-filter: blur(20px);
            padding: 20px 45px; border-radius: 20px; border: 1px solid var(--border-clr);
            margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .q-badge {
            background: linear-gradient(135deg, #0891b2, #22d3ee);
            color: #020617; padding: 10px 35px; border-radius: 12px;
            font-weight: 900; font-size: 1.4rem; box-shadow: 0 0 20px rgba(34, 211, 238, 0.4);
        }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 25px; }
        .kpi-card {
            background: var(--card-bg); border-radius: 22px; padding: 20px;
            text-align: center; border: 2px solid var(--border-clr);
            transition: all 0.4s ease; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .kpi-title { font-size: 0.85rem; font-weight: 700; color: var(--text-dim); text-transform: uppercase; margin-bottom: 10px; }
        .val-large { font-size: 3rem; font-weight: 900; line-height: 1; margin-bottom: 8px; }
        .safe { color: var(--neon-blue); text-shadow: 0 0 15px rgba(34, 211, 238, 0.4); }
        .alert { color: var(--neon-red); text-shadow: 0 0 15px rgba(244, 63, 94, 0.4); }
        .bm-container { font-size: 0.75rem; color: #475569; background: rgba(255, 255, 255, 0.05); padding: 4px 12px; border-radius: 6px; }
        .bottom-section { display: grid; grid-template-columns: 2fr 1.1fr; gap: 25px; height: 350px; }
        .glass-panel { background: var(--card-bg); border-radius: 25px; padding: 25px; border: 1px solid var(--border-clr); display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .score-circle { width: 180px; height: 180px; border-radius: 50%; border: 10px solid #1e293b; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: all 1s ease; }
        .score-num { font-size: 3.5rem; font-weight: 900; }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header">
            <div>
                <h1 style="margin:0; font-size:1.6rem;">UNIT: <span style="color:var(--neon-blue)">3FGW-DAMMAM</span></h1>
                <p style="margin:5px 0 0 0; color:var(--text-dim);">QUALITY & SAFETY PERFORMANCE TRACKER</p>
            </div>
            <div class="q-badge" id="qLabel">1Q 2024</div>
        </div>
        <div class="grid" id="kpiGrid"></div>
        <div class="bottom-section">
            <div class="glass-panel"><canvas id="barChartCanvas"></canvas></div>
            <div class="glass-panel">
                <div class="score-circle" id="circleBorder"><div class="score-num" id="scoreVal">0%</div></div>
                <div style="margin-top:15px; font-weight:700; color:var(--text-dim);">OVERALL QUALITY INDEX</div>
            </div>
        </div>
    </div>
    <script>
        // البيانات المستخرجة بدقة من ملف "3FGW-Dammam"
        const clinicalData = [
            { q: "1Q 2024", v: [0.42, 0.00, 0.00, 0.00, 6.47, 4.87, 0.11, 0.00], b: [0.35, 0.12, 0.00, 0.00, 7.38, 7.38, 0.00, 0.00] },
            { q: "2Q 2024", v: [0.00, 0.00, 2.01, 0.00, 7.15, 6.43, 2.00, 0.00], b: [0.64, 0.00, 1.30, 0.90, 6.80, 7.38, 0.35, 0.02] },
            { q: "3Q 2024", v: [1.12, 0.17, 0.00, 3.33, 4.79, 4.21, 9.00, 0.01], b: [0.45, 0.00, 1.15, 0.75, 7.10, 7.10, 0.37, 0.00] },
            { q: "4Q 2024", v: [2.09, 0.00, 0.00, 7.15, 7.02, 7.17, 0.00, 0.01], b: [0.35, 0.08, 1.10, 0.80, 7.00, 7.00, 0.37, 0.02] },
            { q: "3Q 2025", v: [0.10, 0.00, 0.00, 7.40, 6.89, 7.40, 4.00, 0.01], b: [0.43, 0.10, 1.20, 0.85, 7.15, 7.15, 0.40, 0.01] }
        ];

        const kpis = ["Total Falls", "Injury Falls", "CLABSI", "CAUTI", "RN Hours", "Nursing Hours", "Assault Rate", "Injury Assault"];
        let step = 0; let mainChart;

        function update() {
            const current = clinicalData[step];
            document.getElementById('qLabel').innerText = current.q;
            const grid = document.getElementById('kpiGrid');
            grid.innerHTML = '';
            let met = 0;

            current.v.forEach((val, i) => {
                // المؤشرات (4 و 5) هي ساعات التمريض: الأعلى أفضل. الباقي: الأقل أفضل.
                const isHigherBetter = (i === 4 || i === 5);
                const isBad = isHigherBetter ? (val < current.b[i]) : (val > current.b[i]);
                if(!isBad) met++;
                
                grid.innerHTML += `
                    <div class="kpi-card">
                        <div class="kpi-title">${kpis[i]}</div>
                        <div class="val-large ${isBad ? 'alert' : 'safe'}">${val}</div>
                        <div class="bm-container">BM: ${current.b[i]}</div>
                    </div>`;
            });

            const score = Math.round((met/8)*100);
            document.getElementById('scoreVal').innerText = score + "%";
            const color = score >= 70 ? "#22d3ee" : "#f43f5e";
            document.getElementById('scoreVal').style.color = color;
            document.getElementById('circleBorder').style.borderColor = color;

            if(!mainChart) {
                const ctx = document.getElementById('barChartCanvas').getContext('2d');
                mainChart = new Chart(ctx, {
                    type: 'bar',
                    data: { labels: kpis, datasets: [{ data: current.v, backgroundColor: '#22d3ee', borderRadius: 5 }] },
                    options: { maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { grid: { color: 'rgba(255,255,255,0.05)' } } } }
                });
            } else {
                mainChart.data.datasets[0].data = current.v;
                mainChart.update();
            }
            step = (step + 1) % clinicalData.length;
        }
        update(); setInterval(update, 8000);
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=950, scrolling=False)
