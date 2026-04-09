import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(
    page_title="3FGW Dammam Performance",
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
            --card-bg: #0a0a0a;
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
            background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(20px);
            padding: 20px 45px; border-radius: 20px; border: 1px solid var(--border-clr);
            margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .q-badge {
            background: linear-gradient(135deg, #0891b2, #22d3ee);
            color: #020617; padding: 10px 35px; border-radius: 12px;
            font-weight: 900; font-size: 1.4rem; box-shadow: 0 0 20px rgba(34, 211, 238, 0.4);
        }

        /* المربعات والدوائر مع حركة الموسيقى المتوهجة */
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 25px; }

        .kpi-card, .score-circle {
            position: relative; background-color: var(--card-bg); 
            overflow: hidden; border: 2px solid #1a1a1a;
            transition: all 0.4s ease;
        }

        .kpi-card { border-radius: 22px; padding: 25px; text-align: center; height: 180px; }
        
        .score-circle { 
            width: 200px; height: 200px; border-radius: 50%; 
            display: flex; flex-direction: column; align-items: center; 
            justify-content: center; margin: auto; 
        }

        /* تأثير "حركة الموسيقى" النيوني */
        .kpi-card::before, .score-circle::before {
            content: ''; position: absolute; width: 250%; height: 250%;
            background: conic-gradient(var(--neon-blue), #001a1a, var(--neon-blue));
            animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
        }

        .kpi-card::after, .score-circle::after {
            content: ''; position: absolute; background-color: var(--card-bg); 
            inset: 4px; border-radius: 18px; z-index: 1;
        }
        .score-circle::after { border-radius: 50%; inset: 8px; }

        @keyframes rotate-wave { 
            0% { transform: translate(-50%, -50%) rotate(0deg); } 
            100% { transform: translate(-50%, -50%) rotate(360deg); } 
        }

        /* ضمان ظهور المحتوى فوق الحركة */
        .content-z { position: relative; z-index: 10; }

        .kpi-title { font-size: 0.85rem; font-weight: 700; color: var(--text-dim); text-transform: uppercase; margin-bottom: 10px; }
        .val-large { font-size: 3rem; font-weight: 900; line-height: 1; margin-bottom: 8px; }
        .safe { color: var(--neon-blue); text-shadow: 0 0 15px rgba(34, 211, 238, 0.4); }
        .alert { color: var(--neon-red); text-shadow: 0 0 15px rgba(244, 63, 94, 0.4); }
        .bm-container { font-size: 0.75rem; color: #475569; background: rgba(255, 255, 255, 0.05); padding: 4px 12px; border-radius: 6px; display: inline-block; }

        .bottom-section { display: grid; grid-template-columns: 2fr 1.1fr; gap: 25px; height: 380px; }
        .glass-panel { background: rgba(15, 23, 42, 0.8); border-radius: 25px; padding: 30px; border: 1px solid var(--border-clr); display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .score-num { font-size: 4rem; font-weight: 900; }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header">
            <div>
                <h1 style="margin:0; font-size:1.8rem;">UNIT: <span style="color:var(--neon-blue)">3FGW-DAMMAM</span></h1>
                <p style="margin:5px 0 0 0; color:var(--text-dim); font-weight:600;">QUALITY & SAFETY PERFORMANCE</p>
            </div>
            <div class="q-badge" id="qLabel">1Q 2024</div>
        </div>

        <div class="grid" id="kpiGrid"></div>

        <div class="bottom-section">
            <div class="glass-panel"><canvas id="barChartCanvas"></canvas></div>
            <div class="glass-panel">
                <div class="score-circle">
                    <div class="score-num content-z" id="scoreVal">0%</div>
                </div>
                <div class="content-z" style="margin-top:20px; font-weight:700; color:var(--text-dim);">OVERALL QUALITY SCORE</div>
            </div>
        </div>
    </div>

    <script>
        // داتا فرع الدمام الصحيحة
        const clinicalData = [
            { q: "1Q 2024", v: [0.42, 0.00, 0.00, 0.00, 6.47, 4.87, 0.00, 0.00], b: [0.35, 0.12, 1.25, 0.88, 7.38, 7.38, 0.11, 0.04] },
            { q: "2Q 2024", v: [0.00, 0.00, 2.01, 0.00, 7.15, 6.43, 2.00, 0.00], b: [0.64, 0.00, 1.30, 0.90, 6.80, 7.38, 0.35, 0.02] },
            { q: "3Q 2024", v: [1.12, 0.17, 0.00, 3.33, 4.79, 4.21, 9.00, 0.01], b: [0.45, 0.00, 1.15, 0.75, 7.10, 7.10, 0.37, 0.00] },
            { q: "4Q 2024", v: [2.09, 0.00, 0.00, 7.15, 7.02, 7.17, 0.00, 0.01], b: [0.35, 0.08, 1.10, 0.80, 7.00, 7.00, 0.37, 0.02] }
        ];

        const kpis = ["Falls", "Injury Falls", "CLABSI", "CAUTI", "RN Hours", "Nursing Hours", "Assault", "Injury Assault"];
        let step = 0; let mainChart;

        function update() {
            const current = clinicalData[step];
            document.getElementById('qLabel').innerText = current.q;
            const grid = document.getElementById('kpiGrid');
            grid.innerHTML = '';
            let met = 0;

            current.v.forEach((val, i) => {
                const isPositive = (i === 4 || i === 5); // ساعات التمريض الأعلى أفضل
                const isBad = isPositive ? (val < current.b[i]) : (val > current.b[i]);
                if(!isBad) met++;
                
                grid.innerHTML += `
                    <div class="kpi-card">
                        <div class="content-z">
                            <div class="kpi-title">${kpis[i]}</div>
                            <div class="val-large ${isBad ? 'alert' : 'safe'}">${val}</div>
                            <div class="bm-container">Benchmark: ${current.b[i]}</div>
                        </div>
                    </div>`;
            });

            const score = Math.round((met/8)*100);
            const scoreEl = document.getElementById('scoreVal');
            scoreEl.innerText = score + "%";
            scoreEl.style.color = score >= 75 ? "#22d3ee" : "#f43f5e";

            if(!mainChart) {
                const ctx = document.getElementById('barChartCanvas').getContext('2d');
                mainChart = new Chart(ctx, {
                    type: 'bar',
                    data: { 
                        labels: kpis, 
                        datasets: [{ data: current.v, backgroundColor: '#22d3ee', borderRadius: 6 }] 
                    },
                    options: { 
                        maintainAspectRatio: false, 
                        plugins: { legend: { display: false } },
                        scales: { y: { grid: { color: 'rgba(255,255,255,0.05)' } } }
                    }
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

components.html(dashboard_html, height=1000, scrolling=False)
