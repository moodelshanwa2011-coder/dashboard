import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Riyadh | Ultra-Pro Dashboard", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #01040a;
            --card-bg: rgba(13, 17, 23, 0.95);
            --neon-blue: #00d2ff;
            --neon-green: #39ff14;
            --danger: #ff003c;
            --border-glow: rgba(0, 210, 255, 0.3);
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg); color: #e6edf3; margin: 0; padding: 10px; overflow: hidden;
        }

        /* تصميم الحدود الاحترافية */
        .glass-panel {
            background: var(--card-bg);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0,0,0,0.5);
            position: relative;
            transition: border 0.5s ease;
        }
        .glass-panel:hover { border-color: var(--neon-blue); box-shadow: 0 0 20px var(--border-glow); }

        /* الهيكل التنظيمي للمربعات */
        .main-layout {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-auto-rows: minmax(140px, auto);
            gap: 12px;
            margin-bottom: 12px;
        }

        .category-title {
            font-size: 0.75rem; font-weight: 900; color: var(--neon-blue);
            text-transform: uppercase; letter-spacing: 1.5px;
            margin-bottom: 12px; padding-left: 10px; border-left: 3px solid var(--neon-blue);
        }

        /* مربعات الأرقام (بدون انقطاع في الحركة) */
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; }
        
        .stat-box {
            background: rgba(255,255,255,0.02);
            padding: 8px; border-radius: 8px; text-align: center;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .val-num {
            font-size: 1.6rem; font-weight: 800; display: block;
            transition: all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1); /* حركة سلسة جداً */
        }
        .label-txt { font-size: 0.6rem; color: #8b949e; text-transform: uppercase; margin-top: 4px; display: block; }
        .bm-txt { font-size: 0.55rem; color: #484f58; display: block; }

        /* القسم السفلي: بار نحيف + دائرة الأمان */
        .bottom-section {
            display: grid;
            grid-template-columns: 2.5fr 1fr;
            gap: 12px;
            height: 200px;
        }

        .visualizer-container {
            padding: 15px; display: flex; align-items: center;
        }

        .safety-circle-box {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
        }

        .circle-svg { width: 130px; height: 130px; transform: rotate(-90deg); }
        .circle-bg { fill: none; stroke: #161b22; stroke-width: 10; }
        .circle-progress {
            fill: none; stroke: var(--neon-blue); stroke-width: 10;
            stroke-linecap: round; transition: stroke-dashoffset 1.5s ease;
        }
        .circle-text {
            position: absolute; font-size: 1.8rem; font-weight: 900; color: var(--neon-blue);
        }

        .safe { color: var(--neon-blue); }
        .warn { color: var(--danger); }
    </style>
</head>
<body>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; padding:0 10px;">
        <h2 style="margin:0; font-size:1rem; letter-spacing:2px;">ICU UNIT <span style="color:var(--neon-blue)">PERFORMANCE MONITOR</span></h2>
        <div id="qDisplay" style="background:var(--neon-blue); color:#000; padding:4px 15px; border-radius:6px; font-weight:900; font-size:0.9rem;">LOADING...</div>
    </div>

    <div class="main-layout" id="gridContainer"></div>

    <div class="bottom-section">
        <div class="glass-panel visualizer-container">
            <canvas id="barChart"></canvas>
        </div>
        <div class="glass-panel safety-circle-box">
            <div style="position:relative; display:flex; align-items:center; justify-content:center;">
                <svg class="circle-svg">
                    <circle class="circle-bg" cx="65" cy="65" r="55"></circle>
                    <circle id="progCircle" class="circle-progress" cx="65" cy="65" r="55" stroke-dasharray="345.5" stroke-dashoffset="345.5"></circle>
                </svg>
                <div class="circle-text" id="safetyVal">0%</div>
            </div>
            <div style="font-size:0.7rem; font-weight:bold; color:#8b949e; margin-top:5px;">UNIT SAFETY INDEX</div>
        </div>
    </div>

    <script>
        const clinicalData = [
            {
                q: "4Q 2023", safety: 88,
                groups: [
                    { title: "Falls Analysis", items: [["Total", 0, 0.04], ["Injury", 0, 0.03]] },
                    { title: "Pressure Injury", items: [["HAPI %", 7.3, 26.6]] },
                    { title: "Infections", items: [["CLABSI", 1.38, 1.3], ["CAUTI", 0, 0.46], ["VAE", 1.57, 1.06]] },
                    { title: "Nursing Staff", items: [["BSN %", 67.2, 83.5], ["Turnover", 5.21, 1.6]] }
                ]
            },
            {
                q: "1Q 2024", safety: 92,
                groups: [
                    { title: "Falls Analysis", items: [["Total", 0.24, 0.09], ["Injury", 0.1, 0.04]] },
                    { title: "Pressure Injury", items: [["HAPI %", 6.45, 7.7]] },
                    { title: "Infections", items: [["CLABSI", 1.28, 2.67], ["CAUTI", 0.7, 0.99], ["VAE", 2.17, 2.42]] },
                    { title: "Nursing Staff", items: [["BSN %", 83.0, 70.3], ["Turnover", 4.84, 4.49]] }
                ]
            }
        ];

        let step = 0;
        let chart;

        function update() {
            const data = clinicalData[step];
            document.getElementById('qDisplay').innerText = data.q;
            
            // تحديث المربعات
            const grid = document.getElementById('gridContainer');
            grid.innerHTML = '';
            data.groups.forEach(g => {
                let statsHtml = g.items.map(i => {
                    const isSafe = (i[0].includes("%")) ? (i[1] >= i[2]) : (i[1] <= i[2]);
                    return `
                        <div class="stat-box">
                            <span class="val-num ${isSafe?'safe':'warn'}">${i[1]}</span>
                            <span class="label-txt">${i[0]}</span>
                            <span class="bm-txt">Target: ${i[2]}</span>
                        </div>`;
                }).join('');
                grid.innerHTML += `<div class="glass-panel" style="padding:15px;"><div class="category-title">${g.title}</div><div class="stats-grid">${statsHtml}</div></div>`;
            });

            // تحديث دائرة الأمان
            const offset = 345.5 - (345.5 * data.safety / 100);
            document.getElementById('progCircle').style.strokeDashoffset = offset;
            document.getElementById('safetyVal').innerText = data.safety + "%";

            // تحديث البار (Visualizer) - نحيف وحديث
            const barVals = data.groups.map(g => g.items[0][1]);
            if(!chart) {
                const ctx = document.getElementById('barChart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'bar',
                    data: { labels: data.groups.map(g => g.title), datasets: [{ data: barVals, backgroundColor: '#00d2ff', borderRadius: 20 }] },
                    options: { 
                        maintainAspectRatio: false, 
                        plugins: { legend: { display: false } },
                        scales: { x: { grid: { display: false } }, y: { display: false } }
                    }
                });
            } else {
                chart.data.datasets[0].data = barVals;
                chart.update();
            }

            step = (step + 1) % clinicalData.length;
        }

        update();
        setInterval(update, 15000); // كل 15 ثانية كما طلبت
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=800, scrolling=False)
