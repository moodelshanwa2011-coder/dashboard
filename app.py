import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون بملء الشاشة وبدون هوامش
st.set_page_config(
    page_title="ICU Dammam | Executive Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# دمج داتا الدمام المستخرجة من الملف في هيكل الـ HTML
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
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 25px;
            overflow: hidden;
        }

        .dashboard-container { max-width: 1580px; margin: 0 auto; }

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
            border: 2px solid var(--border-clr);
            position: relative;
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
            letter-spacing: 1px;
        }

        .val-large {
            font-size: 3.2rem;
            font-weight: 900;
            line-height: 1;
            margin-bottom: 10px;
        }

        .safe { color: var(--neon-blue); text-shadow: 0 0 15px rgba(34, 211, 238, 0.4); }
        .alert { color: var(--neon-red); text-shadow: 0 0 15px rgba(244, 63, 94, 0.4); }

        .bm-container {
            font-size: 0.8rem;
            font-weight: 600;
            color: #475569;
            background: rgba(255, 255, 255, 0.05);
            padding: 5px 15px;
            border-radius: 8px;
            display: inline-block;
        }

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
        .score-txt { font-size: 1.1rem; font-weight: 700; color: var(--text-dim); margin-top: 15px; }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header">
            <div>
                <h1 style="margin:0; font-size:1.8rem; letter-spacing:1px;">ICU <span style="color:var(--neon-blue)">DAMMAM</span> TRACKER</h1>
                <p style="margin:5px 0 0 0; color:var(--text-dim); font-weight:600;">SAUDI GERMAN HEALTH | 3FGW-DAMMAM</p>
            </div>
            <div class="q-badge" id="qLabel">1Q 2024</div>
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
                <div class="score-txt">OVERALL SAFETY SCORE</div>
                <p style="color:#475569; font-size:0.75rem; margin-top:10px;">Dammam Branch Performance Data</p>
            </div>
        </div>
    </div>

    <script>
        // داتا الدمام (Dammam ICU Data) المستخرجة من ملف PDF
        const clinicalData = [
            { q: "1Q 2024", v: [0.42, 0.00, 4.38, 0.00, 0.00, 0.00, 85.0, 7.38], b: [0.35, 0.12, 7.00, 1.25, 0.88, 1.34, 78.5, 7.00] },
            { q: "2Q 2024", v: [0.00, 0.00, 7.15, 2.01, 0.00, 0.00, 82.0, 6.41], b: [0.64, 0.00, 6.80, 1.30, 0.90, 1.40, 80.0, 7.38] },
            { q: "3Q 2024", v: [1.12, 0.17, 4.79, 0.00, 3.33, 0.00, 75.0, 6.41], b: [0.45, 0.00, 7.10, 1.15, 0.75, 1.20, 83.0, 7.10] },
            { q: "4Q 2024", v: [2.09, 0.00, 7.02, 0.00, 7.15, 0.00, 88.0, 4.52], b: [0.35, 0.08, 7.00, 1.10, 0.80, 1.25, 85.0, 7.00] },
            { q: "3Q 2025", v: [0.10, 0.00, 6.89, 0.00, 7.40, 0.00, 90.0, 3.33], b: [0.43, 0.10, 7.15, 1.20, 0.85, 1.30, 84.0, 7.15] }
        ];

        const kpis = ["Falls", "Injury Falls", "Nursing Hr", "CLABSI", "CAUTI", "VAE", "RN Edu %", "Total Hr"];
        let step = 0; let mainChart;

        function update() {
            const current = clinicalData[step];
            document.getElementById('qLabel').innerText = current.q;
            const grid = document.getElementById('kpiGrid');
            grid.innerHTML = '';
            let met = 0;

            current.v.forEach((val, i) => {
                // منطق المؤشرات: (Falls/CLABSI الخ) الأقل أفضل، (Education/Nursing) الأعلى أفضل
                const isPositiveKPI = (i === 2 || i === 6 || i === 7); 
                const isBad = isPositiveKPI ? (val < current.b[i]) : (val > current.b[i]);
                
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
            const scoreEl = document.getElementById('scoreVal');
            const ring = document.getElementById('circleBorder');
            
            scoreEl.innerText = score + "%";
            const color = score >= 75 ? "#22d3ee" : "#f43f5e";
            scoreEl.style.color = color;
            ring.style.borderColor = color;
            ring.style.boxShadow = `0 0 35px ${color}44`;

            if(!mainChart) {
                const ctx = document.getElementById('barChartCanvas').getContext('2d');
                mainChart = new Chart(ctx, {
                    type: 'bar',
                    data: { 
                        labels: kpis, 
                        datasets: [{ data: current.v, backgroundColor: '#22d3ee', borderRadius: 6, barThickness: 25 }] 
                    },
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
                mainChart.data.datasets[0].data = current.v;
                mainChart.update();
            }
            step = (step + 1) % clinicalData.length;
        }
        update(); setInterval(update, 8000); // تحديث كل 8 ثوانٍ بنفس وتيرة تصميمك
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=1000, scrolling=False)
