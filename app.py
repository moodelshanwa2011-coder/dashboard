import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون بملء الشاشة وبدون هوامش
st.set_page_config(
    page_title="SGH Riyadh ICU | Performance Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# كود الواجهة الديناميكي (HTML/CSS/JS)
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #030712;
            --card-bg: rgba(16, 24, 48, 0.7);
            --neon-blue: #00e5ff;
            --danger: #ff0055;
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
            --border-grid: rgba(255, 255, 255, 0.05); /* حدود المربعات الصغيرة */
        }
        
        body {
            font-family: 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0; padding: 10px; overflow: hidden;
            /* إضافة المربعات الصغيرة في الخلفية (PRO GRID) */
            background-image: 
                linear-gradient(var(--border-grid) 1px, transparent 1px),
                linear-gradient(90deg, var(--border-grid) 1px, transparent 1px);
            background-size: 25px 25px; /* حجم المربعات الصغيرة */
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 10px 30px; background: var(--card-bg); backdrop-filter: blur(15px);
            border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 15px;
        }

        .q-badge {
            background: rgba(0, 229, 255, 0.1); color: var(--neon-blue);
            border: 1px solid var(--neon-blue); padding: 5px 20px;
            border-radius: 8px; font-weight: 800; font-size: 1rem;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px; margin-bottom: 15px;
        }

        .mega-card {
            background: var(--card-bg); backdrop-filter: blur(10px);
            border-radius: 20px; padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.03);
            position: relative; transition: 0.3s;
        }

        .span-2 { grid-column: span 2; }

        .category-title { font-size: 0.8rem; font-weight: 900; color: var(--neon-blue); text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 15px; }

        .tiles-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; }
        
        .tile { background: rgba(255,255,255,0.01); padding: 10px; border-radius: 10px; text-align: center; border: 1px solid rgba(255,255,255,0.02); }

        .tile-val { font-size: 1.8rem; font-weight: 900; display: block; }
        .tile-label { font-size: 0.6rem; color: var(--text-dim); text-transform: uppercase; margin-top: 5px; }
        .tile-bm { font-size: 0.55rem; color: #475569; display: block; margin-top: 3px; }

        .safe { color: var(--neon-blue); text-shadow: 0 0 10px rgba(0, 229, 255, 0.3); }
        .warn { color: var(--danger); text-shadow: 0 0 10px rgba(255, 0, 85, 0.3); }

        /* القسم السفلي: بار أفقي + دائرة أمان */
        .footer-row {
            display: grid; grid-template-columns: 3fr 1fr; gap: 15px; height: 180px;
        }

        .chart-box { padding: 10px; display: flex; align-items: center; justify-content: center;}
        
        .safety-box { display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; }

        .ring-svg { width: 110px; height: 110px; transform: rotate(-90deg); }
        .ring-bg { fill: none; stroke: #161b22; stroke-width: 9; }
        .ring-fill {
            fill: none; stroke: var(--neon-blue); stroke-width: 9;
            stroke-linecap: round; transition: stroke-dashoffset 1.5s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .ring-text { position: absolute; font-size: 1.6rem; font-weight: 900; color: var(--neon-blue); }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h2 style="margin:0; font-size:1.2rem; letter-spacing:1px;">ICU RIYADH <span style="color:var(--neon-blue)">| INTEL DASHBOARD</span></h2>
            <p style="margin:3px 0 0 0; color:var(--text-dim); font-size:0.8rem;"> Saudi German Hospital | Critical Operations</p>
        </div>
        <div class="q-badge" id="qLabel">...</div>
    </div>

    <div class="dashboard-grid" id="containerGrid"></div>

    <div class="footer-row">
        <div class="mega-card chart-box">
            <canvas id="liveChart"></canvas>
        </div>
        
        <div class="mega-card safety-box">
            <svg class="ring-svg">
                <circle class="ring-bg" cx="55" cy="55" r="45"></circle>
                <circle id="progRing" class="ring-fill" cx="55" cy="55" r="45" stroke-dasharray="282.6" stroke-dashoffset="282.6"></circle>
            </svg>
            <div class="ring-text" id="safetyScore">0%</div>
            <div style="font-size:0.6rem; color:var(--text-dim); margin-top:5px; font-weight:bold;">UNIT SAFETY INDEX</div>
        </div>
    </div>

    <script>
        // البيانات المستخرجة من جدول PDF
        const fullLog = [
            {
                q: "4Q 2023", safety: 88,
                groups: [
                    { title: "Falls Analysis", class: "", items: [["Total Falls", 0, 0.04], ["Injury Falls", 0, 0.03]] },
                    { title: "Device Infections", class: "span-2", items: [["CLABSI", 1.38, 1.30], ["CAUTI", 0, 0.46], ["VAE", 1.57, 1.06]] },
                    { title: "Workforce", class: "span-2", items: [["BSN %", 67.2, 83.5], ["Turnover", 5.21, 1.6], ["RN Hrs", 13.0, 8.0]] },
                    { title: "Others", class: "", items: [["MDRO", 0, 0], ["Restraints", 23.3, 5.08]] }
                ]
            },
            {
                q: "1Q 2024", safety: 91,
                groups: [
                    { title: "Falls Analysis", class: "", items: [["Total Falls", 0.24, 0.09], ["Injury Falls", 0, 0.04]] },
                    { title: "Device Infections", class: "span-2", items: [["CLABSI", 1.28, 2.67], ["CAUTI", 0.70, 0.99], ["VAE", 2.17, 2.42]] },
                    { title: "Workforce", class: "span-2", items: [["BSN %", 83.0, 70.3], ["Turnover", 4.84, 4.49], ["RN Hrs", 20.1, 19.1]] },
                    { title: "Others", class: "", items: [["MDRO", 0.21, 0], ["Restraints", 6.45, 6.47]] }
                ]
            }
        ];

        let index = 0;
        let proChart;

        function refresh() {
            const data = fullLog[index];
            document.getElementById('qLabel').innerText = data.q;
            
            // تحديث المربعات
            const grid = document.getElementById('containerGrid');
            grid.innerHTML = '';
            data.groups.forEach(g => {
                let tiles = g.items.map(i => {
                    const isSafe = (i[0].includes("BSN") || i[0].includes("Hrs")) ? (i[1] >= i[2]) : (i[1] <= i[2]);
                    return `<div class="tile">
                        <span class="tile-val ${isSafe?'safe':'warn'}">${i[1]}</span>
                        <span class="tile-label">${i[0]}</span>
                        <span class="tile-bm">BM: ${i[2]}</span>
                    </div>`;
                }).join('');
                grid.innerHTML += `<div class="mega-card ${g.class}"><div class="category-title">${g.title}</div><div class="tiles-container">${tiles}</div></div>`;
            });

            // تحديث الدائرة
            const offset = 282.6 - (282.6 * data.safety / 100);
            document.getElementById('progRing').style.strokeDashoffset = offset;
            document.getElementById('safetyScore').innerText = data.safety + "%";

            // تحديث البار الأفقي (Horizontal Bar Chart)
            const cVals = data.groups.map(g => g.items[0][1]);
            if(!proChart) {
                const ctx = document.getElementById('liveChart').getContext('2d');
                proChart = new Chart(ctx, {
                    type: 'bar', // النوع هو 'bar'
                    data: {
                        labels: data.groups.map(g => g.title),
                        datasets: [{ data: cVals, backgroundColor: '#00e5ff', borderRadius: 5, barThickness: 15 }]
                    },
                    options: {
                        indexAxis: 'y', // قلب الرسم البياني ليكون أفقياً (كما طلبت)
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 10 } } },
                            x: { beginAtZero: true, grid: { display: false }, ticks: { display: false } } // حذف أرقام الطول
                        }
                    }
                });
            } else {
                proChart.data.datasets[0].data = cVals;
                proChart.update();
            }
            index = (index + 1) % fullLog.length;
        }

        refresh();
        setInterval(refresh, 20000); // تحديث كل 20 ثانية
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=1000, scrolling=False)
