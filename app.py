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
            --grid-line: rgba(0, 242, 255, 0.25);
            --border: rgba(0, 242, 255, 0.6);
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            background-image: 
                linear-gradient(var(--grid-line) 2px, transparent 2px),
                linear-gradient(90deg, var(--grid-line) 2px, transparent 2px);
            background-size: 45px 45px;
            color: #fff; margin: 0; padding: 20px; overflow: hidden;
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--panel-bg); padding: 12px 35px; border-radius: 12px;
            border: 2px solid var(--border); margin-bottom: 20px;
        }

        .main-grid {
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 15px; margin-bottom: 20px;
        }

        .panel {
            background: var(--panel-bg); border: 2.5px solid var(--border);
            border-radius: 18px; padding: 20px; backdrop-filter: blur(15px);
            display: flex; flex-direction: column;
        }

        .span-2 { grid-column: span 2; }

        .panel-title {
            font-size: 0.95rem; font-weight: 900; color: var(--safe-blue);
            text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 15px;
            border-left: 6px solid var(--safe-blue); padding-left: 12px;
        }

        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; }
        
        .box {
            background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px; padding: 15px; text-align: center;
        }

        .val { font-size: 2.2rem; font-weight: 900; display: block; line-height: 1; }
        .lbl { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-top: 8px; font-weight: 800; }
        .bm-label { font-size: 0.65rem; color: #475569; display: block; margin-top: 6px; font-weight: bold; border-top: 1px solid #333; padding-top: 4px; }

        .footer { display: grid; grid-template-columns: 2.5fr 1.5fr; gap: 20px; height: 320px; }

        .ring-container { position: relative; width: 200px; height: 200px; margin: auto; }
        .ring-text { 
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
            font-size: 2.8rem; font-weight: 900; color: var(--safe-blue); 
        }
        
        .ring-svg { transform: rotate(-90deg); width: 100%; height: 100%; }
        .ring-track { fill: none; stroke: var(--danger-red); stroke-width: 14; } 
        .ring-progress { 
            fill: none; stroke: var(--safe-blue); stroke-width: 14; 
            stroke-dasharray: 283; stroke-dashoffset: 283; 
            stroke-linecap: butt; transition: stroke-dashoffset 1.5s ease;
        }
    </style>
</head>
<body>

<div class="header">
    <div style="font-size: 1.4rem; font-weight: 900;">SGH RIYADH <span style="color:var(--safe-blue)">| COMMAND CENTER</span></div>
    <div id="qLabel" style="background: var(--safe-blue); color: #000; padding: 6px 25px; border-radius: 8px; font-weight: 900; font-size: 1.1rem;">...</div>
</div>

<div class="main-grid" id="mainGrid"></div>

<div class="footer">
    <div class="panel">
        <div class="panel-title">KPI Achievement Monitor</div>
        <div style="flex-grow: 1; position: relative;">
            <canvas id="horizChart"></canvas>
        </div>
    </div>
    
    <div class="panel" style="display:flex; flex-direction: row; align-items:center; justify-content:center; gap:30px;">
        <div class="ring-container">
            <svg class="ring-svg" viewBox="0 0 100 100">
                <circle class="ring-track" cx="50" cy="50" r="45"></circle>
                <circle id="safetyRing" class="ring-progress" cx="50" cy="50" r="45"></circle>
            </svg>
            <div id="safetyVal" class="ring-text">0%</div>
        </div>
        <div style="text-align: left;">
            <h3 style="color: var(--safe-blue); margin: 0; font-size: 1.4rem;">UNIT SAFETY</h3>
            <p style="color: #94a3b8; font-size: 0.8rem; margin: 5px 0;">Dynamic Quality Index</p>
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
                { id: "skin", title: "Skin Integrity", items: [["Pressure Injuries", 7.3, 26.6]] }
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
                { id: "skin", title: "Skin Integrity", items: [["Pressure Injuries", 6.45, 7.77]] }
            ]
        }
    ];

    let current = 0;
    let chart;

    function getDynamicColor(val, bm, label) {
        const isBetterHigh = label.includes("BSN") || label.includes("Hours");
        if (isBetterHigh) {
            if (val >= bm) return '#00f2ff';
            if (val >= bm * 0.85) return '#ffea00';
            return '#ff0044';
        } else {
            if (val <= bm) return '#00f2ff';
            if (val <= bm * 1.15) return '#ffea00';
            return '#ff0044';
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
                    datasets: [{ data: d.groups.map(g => g.items[0][1]), backgroundColor: barColors, borderRadius: 6 }]
                },
                options: {
                    indexAxis: 'y', maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { 
                            title: { display: true, text: 'KPI VALUE', color: '#94a3b8', font: { size: 10, weight: 'bold' } },
                            grid: { color: 'rgba(255,255,255,0.05)' }, 
                            ticks: { color: '#94a3b8' } 
                        },
                        y: { 
                            title: { display: true, text: 'BENCHMARKING INDICATORS', color: '#94a3b8', font: { size: 10, weight: 'bold' } },
                            ticks: { color: '#fff', font: { weight: 'bold', size: 10 } } 
                        }
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
