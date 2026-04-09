import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="SGH Riyadh | ICU Intelligence Dashboard",
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
            --bg: #01040a;
            --card: rgba(13, 17, 23, 0.95);
            --neon: #00f2ff;
            --danger: #ff0055;
            --border: rgba(0, 242, 255, 0.3);
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg); color: #fff; margin: 0; padding: 10px; overflow: hidden;
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 10px 25px; background: var(--card); border: 1px solid var(--border);
            border-radius: 12px; margin-bottom: 12px;
        }

        .grid-container {
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 12px; margin-bottom: 12px;
        }

        .panel {
            background: var(--card); border: 2px solid var(--border);
            border-radius: 16px; padding: 15px; position: relative;
        }

        .span-2 { grid-column: span 2; }

        .panel-title {
            font-size: 0.8rem; font-weight: 900; color: var(--neon);
            text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px;
            border-left: 4px solid var(--neon); padding-left: 10px;
        }

        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(115px, 1fr)); gap: 10px; }
        
        .stat-tile {
            background: rgba(255,255,255,0.03); border-radius: 10px;
            padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.05);
        }

        .val { font-size: 1.8rem; font-weight: 900; display: block; }
        .label { font-size: 0.65rem; color: #8b949e; text-transform: uppercase; margin-top: 5px; font-weight: bold; }
        .benchmark { font-size: 0.65rem; color: #484f58; display: block; margin-top: 5px; font-weight: 700; }

        .safe { color: var(--neon); text-shadow: 0 0 10px rgba(0, 242, 255, 0.5); }
        .warn { color: var(--danger); text-shadow: 0 0 10px rgba(255, 0, 85, 0.5); }

        .footer { display: grid; grid-template-columns: 3fr 1fr; gap: 12px; height: 220px; }

        .ring-container { position: relative; width: 130px; height: 130px; margin: auto; }
        .ring-text {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            font-size: 1.7rem; font-weight: 900; color: var(--neon);
        }
    </style>
</head>
<body>
    <div class="header">
        <h2 style="margin:0; font-size:1.1rem; letter-spacing:1px;">ICU COMMAND <span style="color:var(--neon)">| LIVE DATA</span></h2>
        <div id="qText" style="background:var(--neon); color:#000; padding:4px 20px; border-radius:6px; font-weight:900;">...</div>
    </div>

    <div class="grid-container" id="mainGrid"></div>

    <div class="footer">
        <div class="panel" style="padding: 10px 15px 5px 15px;">
            <canvas id="barVisualizer"></canvas>
        </div>
        
        <div class="panel" style="display:flex; align-items:center; justify-content:center; gap:15px;">
            <div class="ring-container">
                <svg viewBox="0 0 100 100" style="transform: rotate(-90deg);">
                    <circle cx="50" cy="50" r="45" fill="none" stroke="#161b22" stroke-width="10"></circle>
                    <circle id="safetyRing" cx="50" cy="50" r="45" fill="none" stroke="#00f2ff" stroke-width="10" 
                            stroke-dasharray="283" stroke-dashoffset="283" stroke-linecap="butt" style="transition: 1.5s ease;"></circle>
                </svg>
                <div id="safetyPercent" class="ring-text">0%</div>
            </div>
            <div style="text-align:left;">
                <div style="font-size:0.8rem; color:#8b949e; font-weight:bold;">SAFETY INDEX</div>
                <div style="font-size:0.6rem; color:#484f58; margin-top:3px;">Full compliance score</div>
            </div>
        </div>
    </div>

    <script>
        const clinicalDB = [
            {
                q: "4Q 2023", safety: 88,
                groups: [
                    { title: "Falls Analysis", class: "", items: [["Total Falls", 0, 0.04], ["Injury Falls", 0, 0.03]] },
                    { title: "Infections", class: "span-2", items: [["CLABSI", 1.38, 1.30], ["CAUTI", 0, 0.46], ["VAE", 1.57, 1.06], ["VAP", 0, 0]] },
                    { title: "Skin Integrity", class: "", items: [["HAPI %", 7.3, 26.6], ["Unit Acq", 0, 0]] },
                    { title: "Workforce", class: "span-2", items: [["BSN %", 67.2, 83.5], ["Turnover", 5.21, 1.6], ["RN Hours", 13.0, 8.0], ["CNA Hours", 1.1, 1.2]] }
                ]
            },
            {
                q: "1Q 2024", safety: 92,
                groups: [
                    { title: "Falls Analysis", class: "", items: [["Total Falls", 0.24, 0.09], ["Injury Falls", 0, 0.04]] },
                    { title: "Infections", class: "span-2", items: [["CLABSI", 1.28, 2.67], ["CAUTI", 0.70, 0.99], ["VAE", 2.17, 2.42], ["VAP", 0, 0]] },
                    { title: "Skin Integrity", class: "", items: [["HAPI %", 6.45, 7.77], ["Unit Acq", 0, 0]] },
                    { title: "Workforce", class: "span-2", items: [["BSN %", 83.0, 70.3], ["Turnover", 4.84, 4.49], ["RN Hours", 20.1, 19.1], ["CNA Hours", 1.5, 1.3]] }
                ]
            }
        ];

        let idx = 0;
        let mainChart;

        function update() {
            const data = clinicalDB[idx];
            document.getElementById('qText').innerText = data.q;
            const grid = document.getElementById('mainGrid');
            grid.innerHTML = '';

            data.groups.forEach(g => {
                let tiles = g.items.map(i => {
                    const isSafe = (i[0].includes("BSN") || i[0].includes("Hours")) ? (i[1] >= i[2]) : (i[1] <= i[2]);
                    return `
                        <div class="stat-tile">
                            <span class="val ${isSafe?'safe':'warn'}">${i[1]}</span>
                            <span class="label">${i[0]}</span>
                            <span class="benchmark">Benchmark: ${i[2]}</span>
                        </div>`;
                }).join('');
                grid.innerHTML += `<div class="panel ${g.class}"><div class="panel-title">${g.title}</div><div class="stats-grid">${tiles}</div></div>`;
            });

            document.getElementById('safetyRing').style.strokeDashoffset = 283 - (283 * data.safety / 100);
            document.getElementById('safetyPercent').innerText = data.safety + "%";

            // تحديث البار ليكون ضخماً ومسطحاً
            const vals = data.groups.map(g => g.items[0][1] + 2);
            if(!mainChart) {
                const ctx = document.getElementById('barVisualizer').getContext('2d');
                mainChart = new Chart(ctx, {
                    type: 'bar',
                    data: { labels: data.groups.map(g => g.title), datasets: [{ data: vals, backgroundColor: '#00f2ff' }] },
                    options: { 
                        maintainAspectRatio: false, animation: { duration: 1500, easing: 'easeInOutQuart' },
                        plugins: { legend: { display: false } },
                        scales: { x: { grid: { display: false }, ticks: { color: '#8b949e', font: { size: 10, weight: 'bold' } } }, y: { display: false } },
                        categoryPercentage: 1.0, barPercentage: 0.9 // أعمدة ضخمة ومتلاصقة
                    }
                });
            } else {
                mainChart.data.datasets[0].data = vals;
                mainChart.update();
            }
            idx = (idx + 1) % clinicalDB.length;
        }

        update();
        setInterval(update, 15000); 
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=900, scrolling=False)
