import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون بملء الشاشة
st.set_page_config(
    page_title="ICU Riyadh Executive Dashboard",
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
            --border-clr: rgba(255, 255, 255, 0.15);
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 25px;
            overflow: hidden;
        }

        .dashboard-container { max-width: 1580px; margin: 0 auto; }

        /* Header Style */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            padding: 20px 45px;
            border-radius: 20px;
            border: 1px solid var(--border-clr);
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .q-badge {
            background: linear-gradient(135deg, #0891b2, #22d3ee);
            color: #020617;
            padding: 10px 35px;
            border-radius: 12px;
            font-weight: 900;
            font-size: 1.4rem;
            box-shadow: 0 0 20px rgba(34, 211, 238, 0.4);
        }

        /* KPI Grid - الحدود واضحة واحترافية جداً هنا */
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 25px;
        }

        .kpi-card {
            background: var(--card-bg);
            border-radius: 22px;
            padding: 25px;
            text-align: center;
            border: 2px solid var(--border-clr); /* حدود واضحة */
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .kpi-card:hover {
            transform: translateY(-8px);
            border-color: var(--neon-blue);
            box-shadow: 0 0 25px rgba(34, 211, 238, 0.2);
        }

        .kpi-title { 
            font-size: 0.9rem; 
            font-weight: 700; 
            color: var(--text-dim); 
            text-transform: uppercase; 
            margin-bottom: 15px;
        }

        .val-large {
            font-size: 3.5rem;
            font-weight: 900;
            line-height: 1;
            margin-bottom: 10px;
        }

        .safe { color: var(--neon-blue); text-shadow: 0 0 15px rgba(34, 211, 238, 0.4); }
        .alert { color: var(--neon-red); text-shadow: 0 0 15px rgba(244, 63, 94, 0.4); }

        /* Benchmark تحت الرقم مباشرة */
        .bm-container {
            font-size: 0.8rem;
            font-weight: 600;
            color: #475569;
            background: rgba(255, 255, 255, 0.05);
            padding: 5px 15px;
            border-radius: 8px;
            display: inline-block;
            border: 1px solid rgba(255,255,255,0.05);
        }

        /* قاع الصفحة - الأعمدة البيانية */
        .bottom-section {
            display: grid;
            grid-template-columns: 2fr 1.1fr;
            gap: 25px;
            height: 380px;
        }

        .glass-panel {
            background: var(--card-bg);
            border-radius: 25px;
            padding: 30px;
            border: 1px solid var(--border-clr);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .score-circle {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            border: 12px solid #1e293b;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transition: all 1s ease;
        }

        .score-num { font-size: 4rem; font-weight: 900; line-height: 1; }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header">
            <div>
                <h1 style="margin:0; font-size:1.8rem; letter-spacing:1px;">ICU <span style="color:var(--neon-blue)">PERFORMANCE</span> MONITOR</h1>
                <p style="margin:5px 0 0 0; color:var(--text-dim); font-weight:600;">SAUDI GERMAN HEALTH | RIYADH</p>
            </div>
            <div class="q-badge" id="qLabel">4Q 2023</div>
        </div>

        <div class="grid" id="kpiGrid"></div>

        <div class="bottom-section">
            <div class="glass-panel">
                <canvas id="barChartCanvas"></canvas>
            </div>
            <div class="glass-panel">
                <div class="score-circle" id="circleBorder">
                    <div class="score-num" id="scoreVal">0%</div>
                </div>
                <div style="margin-top:15px; font-weight:700; color:var(--text-dim);">SAFETY COMPLIANCE</div>
            </div>
        </div>
    </div>

    <script>
        const clinicalData = [
            { q: "4Q 2023", v: [0, 7.30, 1.38, 1.57, 0, 5.21, 67.2, 13.0], b: [0.04, 26.6, 1.3, 1.0, 0.4, 1.6, 83.5, 8.0] },
            { q: "1Q 2024", v: [0.24, 6.45, 1.28, 2.17, 0.70, 4.84, 83.0, 20.1], b: [0.09, 7.7, 2.6, 2.4, 0.9, 4.4, 70.3, 19.1] },
            { q: "2Q 2024", v: [0.06, 6.54, 1.56, 2.04, 0.67, 3.74, 82.7, 18.2], b: [0.24, 14.2, 2.4, 1.0, 0.5, 6.2, 71.2, 12.5] },
            { q: "3Q 2024", v: [0.28, 4.60, 1.20, 1.89, 0.40, 4.51, 83.4, 18.3], b: [0.36, 6.9, 2.6, 1.0, 1.0, 4.6, 68.2, 19.2] }
        ];

        const kpis = ["Falls", "Pressure Injury", "CLABSI", "VAE", "CAUTI", "Turnover", "BSN Education", "RN Hours"];
        let step = 0; let mainChart;

        function update() {
            const current = clinicalData[step];
            document.getElementById('qLabel').innerText = current.q;
            const grid = document.getElementById('kpiGrid');
            grid.innerHTML = '';
            let met = 0;

            current.v.forEach((val, i) => {
                const isBad = (i < 6) ? (val > current.b[i]) : (val < current.b[i]);
                const cls = isBad ? 'alert' : 'safe';
                if(!isBad) met++;
                
                grid.innerHTML += `
                    <div class="kpi-card">
                        <div class="kpi-title">${kpis[i]}</div>
                        <div class="val-large ${cls}">${val}</div>
                        <div class="bm-container">Benchmark: ${current.b[i]}</div>
                    </div>`;
            });

            const score = Math.round((met/8)*100);
            document.getElementById('scoreVal').innerText = score + "%";
            const color = score >= 75 ? "#22d3ee" : "#f43f5e";
            document.getElementById('scoreVal').style.color = color;
            document.getElementById('circleBorder').style.borderColor = color;

            if(!mainChart) {
                const ctx = document.getElementById('barChartCanvas').getContext('2d');
                mainChart = new Chart(ctx, {
                    type: 'bar',
                    data: { labels: kpis, datasets: [{ data: current.v, backgroundColor: '#22d3ee', borderRadius: 6 }] },
                    options: { maintainAspectRatio: false, plugins: { legend: { display: false } } }
                });
            } else {
                mainChart.data.datasets[0].data = current.v;
                mainChart.update();
            }
            step = (step + 1) % clinicalData.length;
        }
        update();
        setInterval(update, 20000); // تحديث كل 20 ثانية كما طلبت
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=1000, scrolling=False)
