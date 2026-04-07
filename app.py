import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ICU Riyadh | Executive Dashboard",
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
            --bg: #050810;
            --card-bg: rgba(15, 23, 42, 0.8);
            --neon-cyan: #22d3ee;
            --neon-rose: #f43f5e;
            --text-main: #f8fafc;
            --text-dim: #64748b;
            --border-glow: rgba(34, 211, 238, 0.3);
        }
        
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 30px;
            overflow: hidden;
            height: 100vh;
        }

        .main-container {
            max-width: 1600px;
            margin: 0 auto;
        }

        /* Header Professional Look */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            padding: 25px 50px;
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .header h1 { margin: 0; font-size: 2rem; letter-spacing: 2px; font-weight: 900; }
        .q-badge {
            background: linear-gradient(135deg, #0891b2, #22d3ee);
            color: #020617;
            padding: 12px 40px;
            border-radius: 15px;
            font-weight: 900;
            font-size: 1.5rem;
            box-shadow: 0 0 25px var(--border-glow);
        }

        /* KPI Grid with Professional Borders */
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }

        .kpi-card {
            background: var(--card-bg);
            border-radius: 24px;
            padding: 30px;
            text-align: center;
            border: 2px solid rgba(255, 255, 255, 0.05);
            transition: all 0.4s ease;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        }

        .kpi-card:hover {
            border-color: var(--neon-cyan);
            box-shadow: 0 0 20px var(--border-glow);
            transform: translateY(-5px);
        }

        .val-display {
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 10px;
            line-height: 1;
        }

        .safe-text { color: var(--neon-cyan); text-shadow: 0 0 15px rgba(34, 211, 238, 0.5); }
        .alert-text { color: var(--neon-rose); text-shadow: 0 0 15px rgba(244, 63, 94, 0.5); }

        .label-text { font-size: 1rem; font-weight: 700; color: var(--text-dim); text-transform: uppercase; }

        /* Bottom Section: Chart + Compliance Gauge */
        .bottom-row {
            display: grid;
            grid-template-columns: 1.8fr 1.2fr;
            gap: 30px;
            height: 400px;
        }

        .panel {
            background: var(--card-bg);
            border-radius: 30px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        /* Large Professional Compliance Circle */
        .compliance-circle {
            width: 220px;
            height: 220px;
            border-radius: 50%;
            border: 12px solid #1e293b;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            transition: all 1s ease;
        }

        .score-num { font-size: 4.5rem; font-weight: 900; line-height: 1; }
        .score-label { font-size: 0.9rem; font-weight: 800; color: var(--text-dim); margin-top: 5px; }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header">
            <div>
                <h1>ICU <span style="color:var(--neon-cyan)">EXECUTIVE</span> PERFORMANCE</h1>
                <p style="margin:5px 0 0 0; color:var(--text-dim); font-weight:600;">SAUDI GERMAN HEALTH | RIYADH BRANCH</p>
            </div>
            <div class="q-badge" id="qLabel">4Q 2023</div>
        </div>

        <div class="grid" id="kpiGrid"></div>

        <div class="bottom-row">
            <div class="panel">
                <canvas id="mainChart"></canvas>
            </div>
            <div class="panel">
                <div class="compliance-circle" id="circleBorder">
                    <div class="score-num" id="scoreValue">0%</div>
                </div>
                <div class="score-label" style="margin-top:20px; font-size:1.2rem; color:var(--text-main)">SAFETY COMPLIANCE</div>
                <p style="color:var(--text-dim); font-size:0.8rem; margin-top:10px;">Calculated against Global NHCI Benchmarks</p>
            </div>
        </div>
    </div>

    <script>
        const timeline = [
            { q: "4Q 2023", v: [0, 7.30, 1.38, 1.57, 0, 5.21, 67.2, 13.0], b: [0.04, 26.6, 1.3, 1.0, 0.4, 1.6, 83.5, 8.0] },
            { q: "1Q 2024", v: [0.24, 6.45, 1.28, 2.17, 0.70, 4.84, 83.0, 20.1], b: [0.09, 7.7, 2.6, 2.4, 0.9, 4.4, 70.3, 19.1] },
            { q: "2Q 2024", v: [0.06, 6.54, 1.56, 2.04, 0.67, 3.74, 82.7, 18.2], b: [0.24, 14.2, 2.4, 1.0, 0.5, 6.2, 71.2, 12.5] },
            { q: "3Q 2024", v: [0.28, 4.60, 1.20, 1.89, 0.40, 4.51, 83.4, 18.3], b: [0.36, 6.9, 2.6, 1.0, 1.0, 4.6, 68.2, 19.2] },
            { q: "1Q 2025", v: [1.59, 4.17, 1.26, 1.91, 0.43, 1.43, 83.8, 18.2], b: [0.12, 4.9, 3.0, 6.6, 0.5, 3.9, 70.0, 19.8] }
        ];

        const labels = ["Falls", "HAPI", "CLABSI", "VAE", "CAUTI", "Turnover", "BSN Edu", "RN Hours"];
        let idx = 0; let chart;

        function refresh() {
            const data = timeline[idx];
            document.getElementById('qLabel').innerText = data.q;
            const grid = document.getElementById('kpiGrid');
            grid.innerHTML = '';
            let pass = 0;

            data.v.forEach((v, i) => {
                const isBad = (i < 6) ? (v > data.b[i]) : (v < data.b[i]);
                const cls = isBad ? 'alert-text' : 'safe-text';
                if(!isBad) pass++;
                grid.innerHTML += `
                    <div class="kpi-card">
                        <div class="val-display ${cls}">${v}</div>
                        <div class="label-text">${labels[i]}</div>
                    </div>`;
            });

            // Update Circle Compliance
            const score = Math.round((pass/8)*100);
            const scoreEl = document.getElementById('scoreValue');
            const circle = document.getElementById('circleBorder');
            scoreEl.innerText = score + "%";
            
            const finalColor = score >= 75 ? "#22d3ee" : "#f43f5e";
            scoreEl.style.color = finalColor;
            circle.style.borderColor = finalColor;
            circle.style.boxShadow = `0 0 30px ${finalColor}44`;

            if(!chart) {
                const ctx = document.getElementById('mainChart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'bar',
                    data: { labels: labels, datasets: [{ data: data.v, backgroundColor: '#22d3ee', borderRadius: 8, barThickness: 25 }] },
                    options: { 
                        maintainAspectRatio: false, 
                        plugins: { legend: { display: false } },
                        scales: { 
                            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } },
                            x: { ticks: { color: '#f8fafc', font: { weight: 'bold' } } }
                        }
                    }
                });
            } else {
                chart.data.datasets[0].data = data.v;
                chart.update();
            }
            idx = (idx + 1) % timeline.length;
        }
        refresh(); setInterval(refresh, 8000);
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=1000, scrolling=False)
