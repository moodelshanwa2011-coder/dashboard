import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Riyadh | Absolute Performance", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #02040a;
            --glass: rgba(17, 25, 40, 0.8);
            --neon: #00f2ff;
            --danger: #ff0055;
            --border: rgba(0, 242, 255, 0.2);
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg); color: #fff; margin: 0; padding: 15px; overflow: hidden;
        }

        /* تصميم الهيكل العضوي - Grid Layout */
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-bottom: 12px;
        }

        .mega-card {
            background: var(--glass);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 12px;
            backdrop-filter: blur(10px);
            transition: all 0.5s ease;
        }
        .mega-card:hover { border-color: var(--neon); box-shadow: 0 0 15px rgba(0, 242, 255, 0.1); }

        /* حجم المربعات حسب البيانات */
        .span-2 { grid-column: span 2; }
        .span-v2 { grid-row: span 2; }

        .category-header {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 5px;
        }

        .category-title { font-family: 'Orbitron'; font-size: 0.7rem; color: var(--neon); letter-spacing: 1px; }

        /* الوحدات الرقمية (Tiles) */
        .tiles-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(90px, 1fr)); gap: 8px; }
        
        .tile {
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.03);
            border-radius: 8px; padding: 8px; text-align: center;
        }

        .val-display {
            font-family: 'Orbitron'; font-size: 1.4rem; font-weight: 900; display: block;
            transition: color 0.5s, transform 0.5s;
        }
        .label-display { font-size: 0.55rem; color: #8b949e; text-transform: uppercase; margin-top: 3px; }
        .bm-display { font-size: 0.5rem; color: #484f58; margin-top: 2px; }

        /* القسم السفلي: بار Equalizer + دائرة أمان */
        .footer-strip {
            display: grid; grid-template-columns: 3fr 1fr; gap: 12px; height: 180px;
        }

        .equalizer-box { padding: 10px; display: flex; align-items: flex-end; }
        
        .safety-ring-container {
            display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative;
        }

        .ring-svg { width: 120px; height: 120px; transform: rotate(-90deg); }
        .ring-bg { fill: none; stroke: #161b22; stroke-width: 8; }
        .ring-fill {
            fill: none; stroke: var(--neon); stroke-width: 8;
            stroke-linecap: round; transition: stroke-dashoffset 1.5s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .ring-text { position: absolute; font-family: 'Orbitron'; font-size: 1.5rem; color: var(--neon); }

        .safe { color: var(--neon); }
        .warn { color: var(--danger); }
    </style>
</head>
<body>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <div style="font-family: 'Orbitron'; font-size: 1rem;">ICU PERFORMANCE <span style="color:var(--neon)">RIYADH</span></div>
        <div id="qLabel" style="border:1px solid var(--neon); color:var(--neon); padding:2px 15px; border-radius:4px; font-weight:bold;">...</div>
    </div>

    <div class="dashboard-grid" id="mainDashboard"></div>

    <div class="footer-strip">
        <div class="mega-card equalizer-box">
            <canvas id="equalizerChart"></canvas>
        </div>
        <div class="mega-card safety-ring-container">
            <svg class="ring-svg">
                <circle class="ring-bg" cx="60" cy="60" r="50"></circle>
                <circle id="safetyRing" class="ring-fill" cx="60" cy="60" r="50" stroke-dasharray="314" stroke-dashoffset="314"></circle>
            </svg>
            <div class="ring-text" id="safetyVal">0%</div>
            <div style="font-size:0.6rem; color:#8b949e; margin-top:5px; font-weight:bold;">UNIT SAFETY SCORE</div>
        </div>
    </div>

    <script>
        const clinicalDatabase = [
            {
                q: "4Q 2023", safety: 87,
                groups: [
                    { title: "Falls Metric", class: "", items: [["Total", 0, 0.04], ["Injury", 0, 0.03]] },
                    { title: "Infections (Device)", class: "span-2", items: [["CLABSI", 1.38, 1.30], ["CAUTI", 0, 0.46], ["VAE", 1.57, 1.06], ["VAP", 0, 0]] },
                    { title: "Skin Integrity", class: "", items: [["HAPI Survey", 7.3, 26.6], ["Unit Acq", 0, 0]] },
                    { title: "Nursing Workforce", class: "span-2", items: [["BSN %", 67.19, 83.53], ["Turnover", 5.21, 1.6], ["RN Hrs", 13.0, 8.0], ["CNA Hrs", 1.1, 1.2]] },
                    { title: "Others", class: "", items: [["Restraints", 23.3, 5.08], ["MDRO", 0, 0]] }
                ]
            },
            {
                q: "1Q 2024", safety: 91,
                groups: [
                    { title: "Falls Metric", class: "", items: [["Total", 0.24, 0.09], ["Injury", 0, 0.04]] },
                    { title: "Infections (Device)", class: "span-2", items: [["CLABSI", 1.28, 2.67], ["CAUTI", 0.70, 0.99], ["VAE", 2.17, 2.42], ["VAP", 0, 0]] },
                    { title: "Skin Integrity", class: "", items: [["HAPI Survey", 6.45, 7.77], ["Unit Acq", 0, 0]] },
                    { title: "Nursing Workforce", class: "span-2", items: [["BSN %", 82.99, 70.31], ["Turnover", 4.84, 4.49], ["RN Hrs", 20.1, 19.1], ["CNA Hrs", 1.5, 1.3]] },
                    { title: "Others", class: "", items: [["Restraints", 6.45, 6.47], ["MDRO", 0.21, 0]] }
                ]
            }
        ];

        let step = 0;
        let eqChart;

        function refresh() {
            const data = clinicalDatabase[step];
            document.getElementById('qLabel').innerText = data.q;
            
            const grid = document.getElementById('mainDashboard');
            grid.innerHTML = '';

            data.groups.forEach(g => {
                let tiles = g.items.map(i => {
                    const isSafe = (i[0].includes("BSN") || i[0].includes("Hrs")) ? (i[1] >= i[2]) : (i[1] <= i[2]);
                    return `
                        <div class="tile">
                            <span class="val-display ${isSafe?'safe':'warn'}">${i[1]}</span>
                            <span class="label-display">${i[0]}</span>
                            <span class="bm-display">BM: ${i[2]}</span>
                        </div>`;
                }).join('');
                grid.innerHTML += `<div class="mega-card ${g.class}"><div class="category-header"><div class="category-title">${g.title}</div></div><div class="tiles-container">${tiles}</div></div>`;
            });

            // تحديث الدائرة
            const offset = 314 - (314 * data.safety / 100);
            document.getElementById('safetyRing').style.strokeDashoffset = offset;
            document.getElementById('safetyVal').innerText = data.safety + "%";

            // تحديث الـ Equalizer
            const eqVals = data.groups.map(g => g.items[0][1]);
            if(!eqChart) {
                const ctx = document.getElementById('equalizerChart').getContext('2d');
                eqChart = new Chart(ctx, {
                    type: 'bar',
                    data: { labels: data.groups.map(g => g.title), datasets: [{ data: eqVals, backgroundColor: '#00f2ff', borderRadius: 4, barThickness: 20 }] },
                    options: { 
                        maintainAspectRatio: false, animation: { duration: 1500, easing: 'easeInOutElastic' },
                        plugins: { legend: { display: false } },
                        scales: { x: { ticks: { color: '#484f58', font: { size: 8 } }, grid: { display: false } }, y: { display: false } }
                    }
                });
            } else {
                eqChart.data.datasets[0].data = eqVals;
                eqChart.update();
            }
            step = (step + 1) % clinicalDatabase.length;
        }

        refresh();
        setInterval(refresh, 15000);
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=850, scrolling=False)
