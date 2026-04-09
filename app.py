import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Command Center | SGH", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #01040a;
            --panel-bg: rgba(13, 22, 42, 0.98);
            --safe-blue: #00f2ff;
            --warn-yellow: #ffea00;
            --danger-red: #ff0044;
            --grid-line: rgba(0, 242, 255, 0.28);
            --border: rgba(0, 242, 255, 0.6);
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            background-image: 
                linear-gradient(var(--grid-line) 2.5px, transparent 2.5px),
                linear-gradient(90deg, var(--grid-line) 2.5px, transparent 2.5px);
            background-size: 55px 55px;
            color: #fff; margin: 0; padding: 20px; overflow: hidden;
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--panel-bg); padding: 15px 40px; border-radius: 15px;
            border: 3px solid var(--border); margin-bottom: 20px;
        }

        .main-grid {
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 20px; margin-bottom: 20px;
        }

        .panel {
            background: var(--panel-bg); border: 3px solid var(--border);
            border-radius: 20px; padding: 25px; backdrop-filter: blur(15px);
            display: flex; flex-direction: column; justify-content: space-between;
        }

        .span-2 { grid-column: span 2; }

        .panel-title {
            font-size: 1.1rem; font-weight: 900; color: var(--safe-blue);
            text-transform: uppercase; letter-spacing: 2px; margin-bottom: 15px;
            border-left: 8px solid var(--safe-blue); padding-left: 15px;
        }

        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 18px; }
        
        .box {
            background: rgba(255,255,255,0.04); border: 1.5px solid rgba(255,255,255,0.15);
            border-radius: 15px; padding: 20px; text-align: center;
        }

        .val { font-size: 2.5rem; font-weight: 900; display: block; line-height: 1; transition: color 0.5s; }
        .lbl { font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; margin-top: 10px; font-weight: 800; }
        .bm-label { font-size: 0.75rem; color: #475569; display: block; margin-top: 8px; font-weight: bold; border-top: 1px solid #333; padding-top: 5px; }

        .footer { display: grid; grid-template-columns: 2.3fr 1.7fr; gap: 25px; height: 380px; }

        .ring-container { position: relative; width: 250px; height: 250px; margin: auto; }
        .ring-text { 
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
            font-size: 3.5rem; font-weight: 900; color: var(--safe-blue); 
        }
        
        .ring-svg { transform: rotate(-90deg); width: 100%; height: 100%; }
        .ring-track { fill: none; stroke: var(--danger-red); stroke-width: 16; } 
        .ring-progress { 
            fill: none; stroke: var(--safe-blue); stroke-width: 16; 
            stroke-dasharray: 283; stroke-dashoffset: 283; 
            stroke-linecap: butt; transition: stroke-dashoffset 1.5s ease;
        }
    </style>
</head>
<body>

<div class="header">
    <div style="font-size: 1.7rem; font-weight: 900; letter-spacing: 3px;">SGH RIYADH <span style="color:var(--safe-blue)">| ICU INTELLIGENT MONITOR</span></div>
    <div id="qLabel" style="background: var(--safe-blue); color: #000; padding: 8px 35px; border-radius: 12px; font-weight: 900; font-size: 1.3rem;">...</div>
</div>

<div class="main-grid" id="mainGrid"></div>

<div class="footer">
    <div class="panel">
        <div class="panel-title">Dynamic Performance Thresholds (X/Y Axis)</div>
        <div style="flex-grow: 1; position: relative;">
            <canvas id="horizChart"></canvas>
        </div>
    </div>
    
    <div class="panel" style="display:flex; flex-direction: row; align-items:center; justify-content:space-around;">
        <div class="ring-container">
            <svg class="ring-svg" viewBox="0 0 100 100">
                <circle class="ring-track" cx="50" cy="50" r="45"></circle>
                <circle id="safetyRing" class="ring-progress" cx="50" cy="50" r="45"></circle>
            </svg>
            <div id="safetyVal" class="ring-text">0%</div>
        </div>
        <div style="text-align: left; min-width: 150px;">
            <h2 style="color: var(--safe-blue); margin: 0; font-size: 1.8rem;">UNIT SAFETY</h2>
            <div style="margin-top: 15px; font-size: 0.95rem; line-height: 1.8;">
                <div style="color: var(--safe-blue); font-weight: 800;">● BLUE: OPTIMAL</div>
                <div style="color: var(--warn-yellow); font-weight: 800;">● YELLOW: CAUTION</div>
                <div style="color: var(--danger-red); font-weight: 800;">● RED: CRITICAL GAP</div>
            </div>
        </div>
    </div>
</div>

<script>
    const clinicalDB = [
        {
            q: "4Q 2023", safety: 88,
            groups: [
                { id: "falls", title: "Falls Analysis", items: [["Total Falls", 0.0, 0.04]] },
                { id: "infect", title: "Infections", class: "span-2", items: [["CLABSI", 1.38, 1.30], ["CAUTI", 0.0, 0.46], ["VAE", 1.57, 1.06]] },
                { id: "staff", title: "Workforce", items: [["BSN %", 67.2, 83.5]] },
                { id: "restr", title: "Restraints Control", items: [["Restraints", 23.3, 5.08]] },
                { id: "hours", title: "Nursing Hours", class: "span-2", items: [["RN Hours", 13.0, 8.0], ["CNA Hours", 1.1, 1.2]] },
                { id: "skin", title: "Skin Health", items: [["Skin Survey", 7.3, 26.6]] }
            ]
        },
        {
            q: "1Q 2024", safety: 94,
            groups: [
                { id: "falls", title: "Falls Analysis", items: [["Total Falls", 0.24, 0.09]] },
                { id: "infect", title: "Infections", class: "span-2", items: [["CLABSI", 1.28, 2.67], ["CAUTI", 0.70, 0.99], ["VAE", 2.17, 2.42]] },
                { id: "staff", title: "Workforce", items: [["BSN %", 83.0, 70.3]] },
                { id: "restr", title: "Restraints Control", items: [["Restraints", 6.45, 6.47]] },
                { id: "hours", title: "Nursing Hours", class: "span-2", items: [["RN Hours", 20.1, 19.1], ["CNA Hours", 1.5, 1.3]] },
                { id: "skin", title: "Skin Health", items: [["Skin Survey", 6.45, 7.77]] }
            ]
        }
    ];

    let current = 0;
    let chart;

    function getDynamicColor(val, bm, label) {
        const isBetterHigh = label.includes("BSN") || label.includes("Hours");
        if (isBetterHigh) {
            if (val >= bm) return '#00f2ff'; // Safe
            if (val >= bm * 0.85) return '#ffea00'; // Caution
            return '#ff0044'; // Danger
        } else {
            if (val <= bm) return '#00f2ff'; // Safe
            if (val <= bm * 1.15) return '#ffea00'; // Caution
            return '#ff0044'; // Danger
        }
    }

    function init() {
        const grid = document.getElementById('mainGrid');
        clinicalDB[0].groups.forEach(g => {
            grid.innerHTML += `<div class="panel ${g.class || ''}"><div class="panel-title">${g.title}</div><div class="stats-grid" id="group-${g.id}"></div></div>`;
        });
        updateData();
    }

    function updateData() {
        const d = clinicalDB[current];
        document.getElementById('qLabel').innerText = d.q;

        d.groups.forEach(g => {
            const groupDiv = document.getElementById(`group-${g.id}`);
            groupDiv.innerHTML = g.items.map(i => {
                const color = getDynamicColor(i[1], i[2], i[0]);
                return `<div class="box">
                    <span class="val" style="color:${color}">${i[1]}</span>
                    <span class="lbl">${i[0]}</span>
                    <span class="bm-label">Benchmark: ${i[2]}</span>
                </div>`;
            }).join('');
        });

        const barColors = d.groups.map(g => getDynamicColor(g.items[0][1], g.items[0][2], g.items[0][0]));

        if(!chart) {
            const ctx = document.getElementById('horizChart').getContext('2d');
            chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: d.groups.map(g => g.title),
                    datasets: [{ data: d.groups.map(g => g.items[0][1]), backgroundColor: barColors, borderRadius: 8 }]
                },
                options: {
                    indexAxis: 'y', maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#94a3b8', font: { size: 12 } } },
                        y: { ticks: { color: '#fff', font: { weight: 'bold', size: 12 } } }
                    }
                }
            });
        } else {
            chart.data.datasets[0].data = d.groups.map(g => g.items[0][1]);
            chart.data.datasets[0].backgroundColor = barColors;
            chart.update();
        }

        document.getElementById('safetyRing').style.strokeDashoffset = 283 - (283 * d.safety / 100);
        document.getElementById('safetyVal').innerText = d.safety + "%";
        current = (current + 1) % clinicalDB.length;
    }

    init();
    setInterval(updateData, 15000);
</script>
</body>
</html>
"""

components.html(dashboard_html, height=1050, scrolling=False)
