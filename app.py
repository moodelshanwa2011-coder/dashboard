import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ICU Executive | Live Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        :root {
            --bg: #020617;
            --card-bg: rgba(15, 23, 42, 0.85);
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

        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--card-bg); backdrop-filter: blur(20px);
            padding: 15px 45px; border-radius: 20px; border: 1px solid var(--border-clr);
            margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .q-badge {
            background: linear-gradient(135deg, #0891b2, #22d3ee);
            color: #020617; padding: 8px 30px; border-radius: 12px;
            font-weight: 900; font-size: 1.2rem;
        }

        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px; }

        .kpi-card {
            background: var(--card-bg); border-radius: 20px; padding: 20px;
            text-align: center; border: 2px solid var(--border-clr);
            transition: 0.4s ease;
        }

        .val-large { font-size: 2.8rem; font-weight: 900; line-height: 1; margin-bottom: 8px; }
        .safe { color: var(--neon-blue); text-shadow: 0 0 10px rgba(34, 211, 238, 0.4); }
        .alert { color: var(--neon-red); text-shadow: 0 0 10px rgba(244, 63, 94, 0.4); }

        /* Weekly Section Styles */
        .bottom-section { display: grid; grid-template-columns: 2.5fr 1fr; gap: 20px; height: 400px; }

        .weekly-panel {
            background: var(--card-bg); border-radius: 25px; padding: 25px;
            border: 1px solid var(--border-clr); display: flex; flex-direction: column;
        }

        .weekly-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; flex-grow: 1; }

        .week-box {
            background: rgba(255,255,255,0.03); border: 1px solid var(--border-clr);
            border-radius: 15px; padding: 15px; display: flex; flex-direction: column;
            justify-content: center; align-items: center; position: relative; overflow: hidden;
        }

        .week-label { font-size: 0.7rem; color: var(--text-dim); font-weight: 800; margin-bottom: 5px; }
        .week-val { font-size: 1.8rem; font-weight: 900; color: var(--neon-blue); }

        /* Music Visualizer Bars */
        .visualizer {
            display: flex; align-items: flex-end; gap: 3px; height: 30px; margin-top: 10px;
        }
        .bar {
            width: 4px; background: var(--neon-blue); border-radius: 2px;
            animation: bounce 1s ease-in-out infinite;
        }
        @keyframes bounce {
            0%, 100% { height: 5px; opacity: 0.3; }
            50% { height: 25px; opacity: 1; }
        }

        .score-circle {
            width: 180px; height: 180px; border-radius: 50%; border: 10px solid #1e293b;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1 style="margin:0; font-size:1.5rem;">ICU <span style="color:var(--neon-blue)">DYNAMIC</span> MONITOR</h1>
            <p id="monthDisplay" style="margin:2px 0 0 0; color:var(--text-dim); font-weight:bold;">MARCH - APRIL 2026</p>
        </div>
        <div class="q-badge" id="qLabel">Q1 2026</div>
    </div>

    <div class="grid" id="kpiGrid"></div>

    <div class="bottom-section">
        <div class="weekly-panel">
            <h3 style="margin: 0 0 15px 0; color: var(--neon-blue); font-size: 0.9rem;">WEEKLY LIVE PERFORMANCE (MARCH/APRIL)</h3>
            <div class="weekly-grid" id="weeklyGrid"></div>
        </div>
        
        <div class="weekly-panel" style="align-items: center; justify-content: center;">
            <div class="score-circle" id="ring">
                <div id="scoreVal" style="font-size: 3.5rem; font-weight: 900;">0%</div>
            </div>
            <div style="margin-top:15px; font-weight:800; color:var(--text-dim);">SAFETY SCORE</div>
        </div>
    </div>

    <script>
        const clinicalData = [
            { q: "MARCH WK1", v: [0.1, 6.2, 1.1, 1.4, 0.2, 4.1, 80, 18], b: [0.2, 7.0, 1.3, 1.5, 0.5, 4.5, 75, 15], w: [0.12, 0.15, 0.08, 0.11] },
            { q: "MARCH WK2", v: [0.0, 5.8, 1.0, 2.1, 0.1, 3.8, 82, 19], b: [0.2, 7.0, 1.3, 1.5, 0.5, 4.5, 75, 15], w: [0.09, 0.11, 0.14, 0.10] },
            { q: "APRIL WK1", v: [0.2, 4.5, 1.4, 1.8, 0.6, 4.2, 85, 20], b: [0.3, 5.0, 1.5, 2.0, 0.8, 4.0, 80, 18], w: [0.22, 0.19, 0.25, 0.18] },
            { q: "APRIL WK2", v: [0.1, 4.2, 1.2, 1.5, 0.3, 3.5, 88, 22], b: [0.3, 5.0, 1.5, 2.0, 0.8, 4.0, 80, 18], w: [0.15, 0.17, 0.20, 0.12] }
        ];

        const kpis = ["Falls", "Pressure", "CLABSI", "VAE", "CAUTI", "Turnover", "BSN Edu", "RN Hours"];
        let step = 0;

        function update() {
            const data = clinicalData[step];
            document.getElementById('qLabel').innerText = data.q;
            
            // 1. Update Top KPIs
            const grid = document.getElementById('kpiGrid');
            grid.innerHTML = '';
            let met = 0;
            data.v.forEach((val, i) => {
                const isBad = (i < 6) ? (val > data.b[i]) : (val < data.b[i]);
                if(!isBad) met++;
                grid.innerHTML += `
                    <div class="kpi-card">
                        <div style="font-size:0.8rem; color:var(--text-dim); font-weight:700;">${kpis[i]}</div>
                        <div class="val-large ${isBad?'alert':'safe'}">${val}</div>
                        <div style="font-size:0.7rem; opacity:0.6;">BM: ${data.b[i]}</div>
                    </div>`;
            });

            // 2. Update Weekly Matrix with Music Bars
            const wGrid = document.getElementById('weeklyGrid');
            wGrid.innerHTML = '';
            data.w.forEach((wv, i) => {
                wGrid.innerHTML += `
                    <div class="week-box">
                        <div class="week-label">WEEK 0${i+1} DATA</div>
                        <div class="week-val">${wv}</div>
                        <div class="visualizer">
                            <div class="bar" style="animation-delay: 0.1s"></div>
                            <div class="bar" style="animation-delay: 0.3s"></div>
                            <div class="bar" style="animation-delay: 0.5s"></div>
                            <div class="bar" style="animation-delay: 0.2s"></div>
                            <div class="bar" style="animation-delay: 0.4s"></div>
                        </div>
                    </div>`;
            });

            // 3. Update Score
            const score = Math.round((met/8)*100);
            document.getElementById('scoreVal').innerText = score + "%";
            const clr = score >= 75 ? "#22d3ee" : "#f43f5e";
            document.getElementById('scoreVal').style.color = clr;
            document.getElementById('ring').style.borderColor = clr;

            step = (step + 1) % clinicalData.length;
        }

        update();
        setInterval(update, 20000); // تحديث كل 20 ثانية
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=1000, scrolling=False)
