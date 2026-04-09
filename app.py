import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(page_title="SGH ICU | Pro Intelligence", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #02040a;
            --panel-bg: rgba(10, 20, 35, 0.95);
            --neon-blue: #00f2ff;
            --neon-red: #ff0044;
            --grid-line: rgba(0, 242, 255, 0.25); /* شبكة أسمك وأوضح */
            --border-panel: rgba(0, 242, 255, 0.5);
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            /* خلفية الشبكة الهندسية السميكة */
            background-image: 
                linear-gradient(var(--grid-line) 2px, transparent 2px),
                linear-gradient(90deg, var(--grid-line) 2px, transparent 2px);
            background-size: 50px 50px;
            color: #fff; margin: 0; padding: 15px; overflow: hidden;
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--panel-bg); padding: 12px 30px; border-radius: 12px;
            border: 2px solid var(--border-panel); margin-bottom: 15px;
        }

        .main-grid {
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 15px; margin-bottom: 15px;
        }

        .panel {
            background: var(--panel-bg); border: 2.5px solid var(--border-panel);
            border-radius: 15px; padding: 18px; backdrop-filter: blur(10px);
        }

        .span-2 { grid-column: span 2; }

        .panel-title {
            font-size: 0.85rem; font-weight: 900; color: var(--neon-blue);
            text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px;
            border-left: 5px solid var(--neon-blue); padding-left: 10px;
        }

        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(115px, 1fr)); gap: 12px; }
        
        .box {
            background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px; padding: 12px; text-align: center;
        }

        .val { font-size: 1.8rem; font-weight: 900; display: block; line-height: 1; }
        .lbl { font-size: 0.65rem; color: #94a3b8; text-transform: uppercase; font-weight: bold; margin-top: 6px; }
        .bm { font-size: 0.6rem; color: #475569; display: block; margin-top: 5px; font-weight: 800; }

        .safe { color: var(--neon-blue); }
        .warn { color: var(--neon-red); }

        /* الفوتر السفلي */
        .footer { display: grid; grid-template-columns: 2.5fr 1.5fr; gap: 15px; height: 260px; }

        /* دائرة الأمان الضخمة بلونين */
        .ring-container { position: relative; width: 180px; height: 180px; margin: auto; }
        .ring-text { 
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
            font-size: 2.5rem; font-weight: 900; color: var(--neon-blue); 
        }
        
        .ring-svg { transform: rotate(-90deg); width: 100%; height: 100%; }
        .ring-track { fill: none; stroke: var(--neon-red); stroke-width: 14; } 
        .ring-progress { 
            fill: none; stroke: var(--neon-blue); stroke-width: 14; 
            stroke-dasharray: 283; stroke-dashoffset: 283; 
            stroke-linecap: butt; transition: 1.5s ease-in-out;
        }
    </style>
</head>
<body>

<div class="header">
    <div style="font-size: 1.3rem; font-weight: 900;">SGH RIYADH <span style="color:var(--neon-blue)">| COMMAND CENTER</span></div>
    <div id="qLabel" style="background: var(--neon-blue); color: #000; padding: 5px 25px; border-radius: 8px; font-weight: 900;">...</div>
</div>

<div class="main-grid" id="mainGrid"></div>

<div class="footer">
    <div class="panel">
        <div class="panel-title">PERFORMANCE BENCHMARKING</div>
        <canvas id="horizChart"></canvas>
    </div>
    
    <div class="panel" style="display:flex; align-items:center; justify-content:center; gap:20px;">
        <div class="ring-container">
            <svg class="ring-svg" viewBox="0 0 100 100">
                <circle class="ring-track" cx="50" cy="50" r="45"></circle>
                <circle id="safetyRing" class="ring-progress" cx="50" cy="50" r="45"></circle>
            </svg>
            <div id="safetyVal" class="ring-text">0%</div>
        </div>
        <div>
            <div style="font-size: 1rem; font-weight: 900; color: #94a3b8;">SAFETY INDEX</div>
            <div style="font-size: 0.6rem; color: var(--neon-red); font-weight: bold; margin-top: 5px;">RED = GAP TO TARGET</div>
        </div>
    </div>
</div>

<script>
    const clinicalDB = [
        {
            q: "4Q 2023", safety: 88,
            groups: [
                { title: "Falls Analysis", class: "", items: [["Total Falls", 0, 0.04], ["Injury Falls", 0, 0.03]] },
                { title: "Device Infections", class: "span-2", items: [["CLABSI", 1.38, 1.30], ["CAUTI", 0, 0.46], ["VAE", 1.57, 1.06], ["VAP", 0, 0]] },
                { title: "Workforce", class: "", items: [["BSN %", 67.2, 83.5], ["Turnover", 5.21, 1.6]] },
                { title: "Restraints", class: "", items: [["Restraints", 23.3, 5.08]] },
                { title: "Nursing Hours", class: "span-2", items: [["RN Hours", 13.0, 8.0], ["CNA Hours", 1.1, 1.2]] },
                { title: "Skin & MDRO", class: "", items: [["Skin Survey", 7.3, 26.6], ["MDRO-MRSA", 0.21, 0]] }
            ]
        },
        {
            q: "1Q 2024", safety: 94,
            groups: [
                { title: "Falls Analysis", class: "", items: [["Total Falls", 0.24, 0.09], ["Injury Falls", 0, 0.04]] },
                { title: "Device Infections", class: "span-2", items: [["CLABSI", 1.28, 2.67], ["CAUTI", 0.70, 0.99], ["VAE", 2.17, 2.42], ["VAP", 0, 0]] },
                { title: "Workforce", class: "", items: [["BSN %", 83.0, 70.3], ["Turnover", 4.84, 4.49]] },
                { title: "Restraints", class: "", items: [["Restraints", 6.45, 6.47]] },
                { title: "Nursing Hours", class: "span-2", items: [["RN Hours", 20.1, 19.1], ["CNA Hours", 1.5, 1.3]] },
                { title: "Skin & MDRO", class: "", items: [["Skin Survey", 6.45, 7.77], ["MDRO-MRSA", 0.22, 0]] }
            ]
        }
    ];

    let current = 0;
    let chart;

    function render() {
        const d = clinicalDB[current];
        document.getElementById('qLabel').innerText = d.q;
        const grid = document.getElementById('mainGrid');
        grid.innerHTML = '';
        d.groups.forEach(g => {
            let tiles = g.items.map(i => {
                const safe = (i[0].includes("BSN") || i[0].includes("Hours")) ? (i[1] >= i[2]) : (i[1] <= i[2]);
                return `<div class="box"><span class="val ${safe?'safe':'warn'}">${i[1]}</span><span class="lbl">${i[0]}</span><span class="bm">Benchmark: ${i[2]}</span></div>`;
            }).join('');
            grid.innerHTML += `<div class="panel ${g.class}"><div class="panel-title">${g.title}</div><div class="stats-grid">${tiles}</div></div>`;
        });

        document.getElementById('safetyRing').style.strokeDashoffset = 283 - (283 * d.safety / 100);
        document.getElementById('safetyVal').innerText = d.safety + "%";

        const colors = ['#00f2ff', '#39ff14', '#ffea00', '#ff9100', '#ff0055', '#a020f0'];
        if(!chart) {
            const ctx = document.getElementById('horizChart').getContext('2d');
            chart = new Chart(ctx, {
                type: 'bar',
                data: { labels: d.groups.map(g => g.title), datasets: [{ data: d.groups.map(g => g.items[0][1] + 1), backgroundColor: colors, borderRadius: 5, barThickness: 15 }] },
                options: { indexAxis: 'y', maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { grid: { display: false }, ticks: { color: '#fff', font: { weight: 'bold', size: 9 } } } } }
            });
        } else {
            chart.data.datasets[0].data = d.groups.map(g => g.items[0][1] + 1);
            chart.update();
        }
        current = (current + 1) % clinicalDB.length;
    }
    render();
    setInterval(render, 15000);
</script>
</body>
</html>
"""

components.html(dashboard_html, height=950, scrolling=False)
