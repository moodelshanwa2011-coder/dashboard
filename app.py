import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Riyadh | Full Intelligence", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #010409;
            --panel-bg: rgba(13, 17, 23, 0.9);
            --neon: #00f2ff;
            --grid-color: rgba(0, 242, 255, 0.12);
            --border: rgba(0, 242, 255, 0.4);
        }
        
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: var(--bg);
            background-image: 
                linear-gradient(var(--grid-color) 1px, transparent 1px),
                linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
            background-size: 35px 35px;
            color: #fff; margin: 0; padding: 15px; overflow: hidden;
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--panel-bg); padding: 10px 25px; border-radius: 12px;
            border: 2px solid var(--border); margin-bottom: 15px;
        }

        /* تقسيم المربعات بشكل يسمح بكل الداتا */
        .main-grid {
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 15px; margin-bottom: 15px;
        }

        .panel {
            background: var(--panel-bg); border: 2px solid var(--border);
            border-radius: 15px; padding: 15px; backdrop-filter: blur(10px);
        }

        .span-2 { grid-column: span 2; }

        .panel-title {
            font-size: 0.8rem; font-weight: 800; color: var(--neon);
            text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;
            border-left: 4px solid var(--neon); padding-left: 8px;
        }

        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 10px; }
        
        .box {
            background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);
            border-radius: 8px; padding: 10px; text-align: center;
        }

        .val { font-size: 1.6rem; font-weight: 900; display: block; line-height: 1.1; }
        .lbl { font-size: 0.6rem; color: #8b949e; text-transform: uppercase; font-weight: bold; margin-top: 4px; }
        .bm { font-size: 0.55rem; color: #484f58; display: block; margin-top: 4px; font-weight: bold; }

        .safe { color: var(--neon); }
        .warn { color: #ff0055; }

        .footer { display: grid; grid-template-columns: 2.8fr 1.2fr; gap: 15px; height: 230px; }

        .ring-container { position: relative; width: 120px; height: 120px; }
        .ring-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 1.6rem; font-weight: 900; color: var(--neon); }
    </style>
</head>
<body>

<div class="header">
    <div style="font-size: 1.1rem; font-weight: 900; letter-spacing: 1px;">SGH RIYADH <span style="color:var(--neon)">| ICU FULL DATA</span></div>
    <div id="qLabel" style="border: 2px solid var(--neon); color: var(--neon); padding: 3px 18px; border-radius: 6px; font-weight: 900;">...</div>
</div>

<div class="main-grid" id="mainGrid"></div>

<div class="footer">
    <div class="panel">
        <canvas id="multiColorChart"></canvas>
    </div>
    
    <div class="panel" style="display:flex; align-items:center; justify-content:center; gap:15px;">
        <div class="ring-container">
            <svg viewBox="0 0 100 100" style="transform: rotate(-90deg);">
                <circle cx="50" cy="50" r="45" fill="none" stroke="#161b22" stroke-width="8"></circle>
                <circle id="safetyRing" cx="50" cy="50" r="45" fill="none" stroke="#00f2ff" stroke-width="8" 
                        stroke-dasharray="283" stroke-dashoffset="283" stroke-linecap="butt" style="transition: 1.5s;"></circle>
            </svg>
            <div id="safetyVal" class="ring-text">0%</div>
        </div>
        <div style="text-align: left;">
            <div style="font-size: 0.75rem; font-weight: 900; color: #8b949e;">SAFETY SCORE</div>
            <div style="font-size: 0.55rem; color: #484f58; font-weight: bold;">TOTAL COMPLIANCE</div>
        </div>
    </div>
</div>

<script>
    const fullData = [
        {
            q: "4Q 2023", safety: 88,
            groups: [
                { title: "Falls Analysis", class: "", items: [["Total Falls", 0, 0.04], ["Injury Falls", 0, 0.03]] },
                { title: "Device Infections", class: "span-2", items: [["CLABSI", 1.38, 1.30], ["CAUTI", 0, 0.46], ["VAE", 1.57, 1.06], ["VAP", 0, 0]] },
                { title: "Workforce", class: "", items: [["BSN %", 67.2, 83.5], ["Turnover", 5.21, 1.6]] },
                { title: "Nursing Hours", class: "span-2", items: [["RN Hours", 13.0, 8.0], ["CNA Hours", 1.1, 1.2]] },
                { title: "Skin & MDRO", class: "span-2", items: [["Skin Survey", 7.3, 26.6], ["MDRO-MRSA", 0.21, 0], ["Restraints", 23.3, 5.08]] }
            ]
        },
        {
            q: "1Q 2024", safety: 92,
            groups: [
                { title: "Falls Analysis", class: "", items: [["Total Falls", 0.24, 0.09], ["Injury Falls", 0, 0.04]] },
                { title: "Device Infections", class: "span-2", items: [["CLABSI", 1.28, 2.67], ["CAUTI", 0.70, 0.99], ["VAE", 2.17, 2.42], ["VAP", 0, 0]] },
                { title: "Workforce", class: "", items: [["BSN %", 83.0, 70.3], ["Turnover", 4.84, 4.49]] },
                { title: "Nursing Hours", class: "span-2", items: [["RN Hours", 20.1, 19.1], ["CNA Hours", 1.5, 1.3]] },
                { title: "Skin & MDRO", class: "span-2", items: [["Skin Survey", 6.45, 7.77], ["MDRO-MRSA", 0.22, 0], ["Restraints", 6.45, 6.47]] }
            ]
        }
    ];

    let currentIdx = 0;
    let chart;

    function update() {
        const d = fullData[currentIdx];
        document.getElementById('qLabel').innerText = d.q;
        
        const grid = document.getElementById('mainGrid');
        grid.innerHTML = '';
        d.groups.forEach(g => {
            let tiles = g.items.map(i => {
                const isSafe = (i[0].includes("BSN") || i[0].includes("Hours")) ? (i[1] >= i[2]) : (i[1] <= i[2]);
                return `<div class="box">
                    <span class="val ${isSafe?'safe':'warn'}">${i[1]}</span>
                    <span class="lbl">${i[0]}</span>
                    <span class="benchmark">Benchmark: ${i[2]}</span>
                </div>`;
            }).join('');
            grid.innerHTML += `<div class="panel ${g.class}"><div class="panel-title">${g.title}</div><div class="stats-grid">${tiles}</div></div>`;
        });

        document.getElementById('safetyRing').style.strokeDashoffset = 283 - (283 * d.safety / 100);
        document.getElementById('safetyVal').innerText = d.safety + "%";

        // بار أفقي بألوان مختلفة لكل قسم
        const barColors = ['#00f2ff', '#39ff14', '#ffea00', '#ff0055', '#ff9100'];
        if(!chart) {
            const ctx = document.getElementById('multiColorChart').getContext('2d');
            chart = new Chart(ctx, {
                type: 'bar',
                data: { labels: d.groups.map(g => g.title), datasets: [{ data: d.groups.map(g => g.items[0][1] + 1), backgroundColor: barColors, borderRadius: 5 }] },
                options: {
                    indexAxis: 'y',
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { display: false },
                        y: { grid: { display: false }, ticks: { color: '#fff', font: { weight: 'bold', size: 9 } } }
                    }
                }
            });
        } else {
            chart.data.datasets[0].data = d.groups.map(g => g.items[0][1] + 1);
            chart.update();
        }
        currentIdx = (currentIdx + 1) % fullData.length;
    }

    update();
    setInterval(update, 15000);
</script>
</body>
</html>
"""

components.html(dashboard_html, height=950, scrolling=False)
