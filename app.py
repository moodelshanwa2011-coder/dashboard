import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Dashboard Monitoring | SGH", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #01040a;
            --panel-bg: rgba(10, 25, 47, 0.95);
            --safe-blue: #00f2ff;
            --warn-yellow: #ffea00;
            --danger-red: #ff0044;
            --grid-line: rgba(0, 242, 255, 0.1);
            --border-glow: #00f2ff;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            background-image: 
                linear-gradient(var(--grid-line) 2px, transparent 2px),
                linear-gradient(90deg, var(--grid-line) 2px, transparent 2px);
            background-size: 50px 50px;
            color: #fff; margin: 0; padding: 15px; overflow: hidden;
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--panel-bg); padding: 15px 40px; border-radius: 12px;
            border: 3px solid var(--safe-blue); margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
        }

        .main-grid {
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 15px; margin-bottom: 15px;
        }

        .panel {
            background: var(--panel-bg); border: 2px solid var(--border-glow);
            border-radius: 15px; padding: 20px; backdrop-filter: blur(10px);
            display: flex; flex-direction: column;
            box-shadow: 0 0 10px rgba(0, 242, 255, 0.1);
        }

        .span-2 { grid-column: span 2; }

        .panel-title {
            font-size: 1.1rem; font-weight: 900; color: var(--safe-blue);
            text-transform: uppercase; letter-spacing: 2px; margin-bottom: 15px;
            border-left: 8px solid var(--safe-blue); padding-left: 15px;
        }

        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 12px; }
        
        .box {
            background: rgba(255,255,255,0.03); border: 2.5px solid rgba(0, 242, 255, 0.4);
            border-radius: 12px; padding: 20px; text-align: center;
            transition: all 0.3s ease;
        }

        .val { font-size: 3.2rem; font-weight: 900; display: block; line-height: 1; margin-bottom: 5px; }
        .lbl { font-size: 0.9rem; color: #cbd5e1; text-transform: uppercase; font-weight: 800; }
        .bm-label { font-size: 0.75rem; color: #94a3b8; display: block; margin-top: 10px; border-top: 1px solid #334155; padding-top: 8px; }

        .footer { display: grid; grid-template-columns: 2.7fr 1.3fr; gap: 15px; height: 380px; }

        .ring-container { position: relative; width: 180px; height: 180px; margin: auto; }
        .ring-text { 
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
            font-size: 3.5rem; font-weight: 900; 
        }
        
        .ring-svg { transform: rotate(-90deg); width: 100%; height: 100%; }
        .ring-track { fill: none; stroke: #1e293b; stroke-width: 14; } 
        .ring-progress { 
            fill: none; stroke-width: 14; 
            stroke-dasharray: 283; stroke-dashoffset: 283; 
            stroke-linecap: round; transition: all 1.5s ease;
        }
    </style>
</head>
<body>

<div class="header">
    <div style="font-size: 1.8rem; font-weight: 900; letter-spacing: 3px;">ICU <span style="color:var(--safe-blue)">DASHBOARD</span> MONITORING</div>
    <div id="qLabel" style="background: var(--safe-blue); color: #000; padding: 8px 30px; border-radius: 8px; font-weight: 900; font-size: 1.3rem;">...</div>
</div>

<div class="main-grid" id="mainGrid"></div>

<div class="footer">
    <div class="panel">
        <div class="panel-title">KPI PERFORMANCE (AUDIO EQUALIZER)</div>
        <div style="flex-grow: 1; position: relative;">
            <canvas id="verticalChart"></canvas>
        </div>
    </div>
    
    <div class="panel" style="display:flex; flex-direction: column; align-items:center; justify-content:center; gap:20px;">
        <div class="ring-container">
            <svg class="ring-svg" viewBox="0 0 100 100">
                <circle class="ring-track" cx="50" cy="50" r="45"></circle>
                <circle id="safetyRing" class="ring-progress" cx="50" cy="50" r="45"></circle>
            </svg>
            <div id="safetyVal" class="ring-text">0%</div>
        </div>
        <div style="text-align: center;">
            <h3 style="color: var(--safe-blue); margin: 0; font-size: 1.4rem; letter-spacing: 2px;">UNIT SAFETY</h3>
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
                { id: "restr", title: "Restraints", items: [["Restraints", 23.3, 5.08]] },
                { id: "hours", title: "Nursing Hours", class: "span-2", items: [["RN Hours", 13.0, 8.0], ["CNA Hours", 1.1, 1.2]] },
                { id: "skin", title: "Pressure Injuries", items: [["Pressure Injuries", 7.3, 26.6]] }
            ]
        },
        {
            q: "1Q 2024", safety: 94,
            groups: [
                { id: "falls", title: "Falls Analysis", items: [["Total Falls", 0.24, 0.09]] },
                { id: "infect", title: "Infections", class: "span-2", items: [["CLABSI", 1.28, 2.67], ["CAUTI", 0.70, 0.99], ["VAE", 2.17, 2.42]] },
                { id: "staff", title: "Workforce", items: [["BSN %", 83.0, 70.3]] },
                { id: "restr", title: "Restraints", items: [["Restraints", 6.45, 6.47]] },
                { id: "hours", title: "Nursing Hours", class: "span-2", items: [["RN Hours", 20.1, 19.1], ["CNA Hours", 1.5, 1.3]] },
                { id: "skin", title: "Pressure Injuries", items: [["Pressure Injuries", 6.45, 7.77]] }
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
            if (!groupDiv) return;
            groupDiv.innerHTML = g.items.map(i => {
                const color = getDynamicColor(i[1], i[2], i[0]);
                return `<div class="box" style="border-color:${color}">
                    <span class="val" style="color:${color}">${i[1]}</span>
                    <span class="lbl">${i[0]}</span>
                    <span class="bm-label">Benchmark: ${i[2]}</span>
                </div>`;
            }).join('');
        });

        const safetyColor = d.safety >= 90 ? '#00f2ff' : d.safety >= 80 ? '#ffea00' : '#ff0044';
        const ringProg = document.getElementById('safetyRing');
        ringProg.style.strokeDashoffset = 283 - (283 * d.safety / 100);
        ringProg.style.stroke = safetyColor;
        document.getElementById('safetyVal').innerText = d.safety + "%";
        document.getElementById('safetyVal').style.color = safetyColor;

        const barColors = d.groups.map(g => getDynamicColor(g.items[0][1], g.items[0][2], g.items[0][0]));

        if(!chart) {
            const ctx = document.getElementById('verticalChart').getContext('2d');
            chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: d.groups.map(g => g.title),
                    datasets: [{ data: d.groups.map(g => g.items[0][1]), backgroundColor: barColors, borderRadius: 10, barThickness: 40 }]
                },
                options: {
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { title: { display: true, text: 'BENCHMARKING INDICATORS', color: '#94a3b8' }, ticks: { color: '#fff' } },
                        y: { title: { display: true, text: 'KPI VALUE', color: '#94a3b8' }, ticks: { color: '#94a3b8' } }
                    }
                },
                plugins: [{
                    id: 'equalizerLines',
                    afterDatasetsDraw: (chart) => {
                        const { ctx } = chart; ctx.save();
                        ctx.strokeStyle = 'rgba(0, 4, 10, 0.8)'; ctx.lineWidth = 3;
                        chart.getDatasetMeta(0).data.forEach((bar) => {
                            for (let yPos = bar.base; yPos > bar.y; yPos -= 10) {
                                ctx.beginPath(); ctx.moveTo(bar.x - bar.width / 2, yPos);
                                ctx.lineTo(bar.x + bar.width / 2, yPos); ctx.stroke();
                            }
                        });
                        ctx.restore();
                    }
                }]
            });
        } else {
            chart.data.datasets[0].data = d.groups.map(g => g.items[0][1]);
            chart.data.datasets[0].backgroundColor = barColors;
            chart.update();
        }
        current = (current + 1) % clinicalDB.length;
    }

    init();
    setInterval(updateData, 10000);
</script>
</body>
</html>
"""

components.html(dashboard_html, height=1050, scrolling=False)
