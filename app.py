import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Command Center", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #01040a;
            --panel-bg: rgba(13, 20, 38, 0.95);
            --neon-blue: #00f2ff;
            --neon-red: #ff0044;
            --grid-line: rgba(0, 242, 255, 0.25);
            --border: rgba(0, 242, 255, 0.5);
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            background-image: 
                linear-gradient(var(--grid-line) 2px, transparent 2px),
                linear-gradient(90deg, var(--grid-line) 2px, transparent 2px);
            background-size: 45px 45px;
            color: #fff; margin: 0; padding: 15px; overflow: hidden;
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--panel-bg); padding: 10px 25px; border-radius: 12px;
            border: 2px solid var(--border); margin-bottom: 15px;
        }

        .main-grid {
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 15px; margin-bottom: 15px;
        }

        .panel {
            background: var(--panel-bg); border: 2.5px solid var(--border);
            border-radius: 15px; padding: 15px; backdrop-filter: blur(10px);
            min-height: 120px;
        }

        .span-2 { grid-column: span 2; }

        .panel-title {
            font-size: 0.8rem; font-weight: 900; color: var(--neon-blue);
            text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 10px;
            border-left: 4px solid var(--neon-blue); padding-left: 8px;
        }

        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; }
        
        .box {
            background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px; padding: 10px; text-align: center;
        }

        .val { font-size: 1.7rem; font-weight: 900; display: block; }
        .lbl { font-size: 0.6rem; color: #94a3b8; text-transform: uppercase; margin-top: 4px; }
        .bm { font-size: 0.55rem; color: #475569; display: block; margin-top: 4px; }

        .footer { display: grid; grid-template-columns: 2.5fr 1.5fr; gap: 15px; height: 280px; }

        /* دائرة الأمان الكبيرة */
        .ring-container { position: relative; width: 180px; height: 180px; margin: auto; }
        .ring-text { 
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
            font-size: 2.5rem; font-weight: 900; color: var(--neon-blue); 
        }
        
        .ring-svg { transform: rotate(-90deg); width: 100%; height: 100%; }
        .ring-track { fill: none; stroke: var(--neon-red); stroke-width: 12; } 
        .ring-progress { 
            fill: none; stroke: var(--neon-blue); stroke-width: 12; 
            stroke-dasharray: 283; stroke-dashoffset: 283; 
            stroke-linecap: butt; transition: stroke-dashoffset 1s ease;
        }
    </style>
</head>
<body>

<div class="header">
    <div style="font-size: 1.2rem; font-weight: 900;">SGH RIYADH <span style="color:var(--neon-blue)">| COMMAND CENTER</span></div>
    <div id="qLabel" style="background: var(--neon-blue); color: #000; padding: 4px 20px; border-radius: 6px; font-weight: 900;">...</div>
</div>

<div class="main-grid" id="mainGrid">
    </div>

<div class="footer">
    <div class="panel">
        <div class="panel-title">Operational Performance Benchmarking</div>
        <div style="height: 200px; position: relative;">
            <canvas id="horizChart"></canvas>
        </div>
    </div>
    
    <div class="panel" style="display:flex; align-items:center; justify-content:center;">
        <div class="ring-container">
            <svg class="ring-svg" viewBox="0 0 100 100">
                <circle class="ring-track" cx="50" cy="50" r="45"></circle>
                <circle id="safetyRing" class="ring-progress" cx="50" cy="50" r="45"></circle>
            </svg>
            <div id="safetyVal" class="ring-text">0%</div>
        </div>
    </div>
</div>

<script>
    const clinicalDB = [
        {
            q: "4Q 2023", safety: 88,
            groups: [
                { id: "falls", title: "Falls Analysis", class: "", items: [["Total Falls", 0, 0.04], ["Injury Falls", 0, 0.03]] },
                { id: "infect", title: "Device Infections", class: "span-2", items: [["CLABSI", 1.38, 1.30], ["CAUTI", 0, 0.46], ["VAE", 1.57, 1.06]] },
                { id: "staff", title: "Workforce", class: "", items: [["BSN %", 67.2, 83.5], ["Turnover", 5.21, 1.6]] },
                { id: "restr", title: "Restraints Control", class: "", items: [["Restraints", 23.3, 5.08]] },
                { id: "hours", title: "Nursing Hours", class: "span-2", items: [["RN Hours", 13.0, 8.0], ["CNA Hours", 1.1, 1.2]] },
                { id: "skin", title: "Skin & MDRO", class: "", items: [["Skin Survey", 7.3, 26.6]] }
            ]
        },
        {
            q: "1Q 2024", safety: 94,
            groups: [
                { id: "falls", title: "Falls Analysis", class: "", items: [["Total Falls", 0.24, 0.09], ["Injury Falls", 0, 0.04]] },
                { id: "infect", title: "Device Infections", class: "span-2", items: [["CLABSI", 1.28, 2.67], ["CAUTI", 0.70, 0.99], ["VAE", 2.17, 2.42]] },
                { id: "staff", title: "Workforce", class: "", items: [["BSN %", 83.0, 70.3], ["Turnover", 4.84, 4.49]] },
                { id: "restr", title: "Restraints Control", class: "", items: [["Restraints", 6.45, 6.47]] },
                { id: "hours", title: "Nursing Hours", class: "span-2", items: [["RN Hours", 20.1, 19.1], ["CNA Hours", 1.5, 1.3]] },
                { id: "skin", title: "Skin & MDRO", class: "", items: [["Skin Survey", 6.45, 7.77]] }
            ]
        }
    ];

    let current = 0;
    let chart;

    // بناء الهيكل الأساسي مرة واحدة فقط لمنع الوميض
    function init() {
        const grid = document.getElementById('mainGrid');
        clinicalDB[0].groups.forEach(g => {
            grid.innerHTML += `
                <div class="panel ${g.class}">
                    <div class="panel-title">${g.title}</div>
                    <div class="stats-grid" id="group-${g.id}"></div>
                </div>`;
        });
        updateData();
    }

    function updateData() {
        const d = clinicalDB[current];
        document.getElementById('qLabel').innerText = d.q;

        // تحديث الأرقام فقط داخل المربعات
        d.groups.forEach(g => {
            const groupDiv = document.getElementById(`group-${g.id}`);
            groupDiv.innerHTML = g.items.map(i => {
                const safe = (i[0].includes("BSN") || i[0].includes("Hours")) ? (i[1] >= i[2]) : (i[1] <= i[2]);
                return `
                    <div class="box">
                        <span class="val ${safe?'':'warn'}" style="color:${safe?'var(--neon-blue)':'var(--neon-red)'}">${i[1]}</span>
                        <span class="lbl">${i[0]}</span>
                        <span class="bm">Benchmark: ${i[2]}</span>
                    </div>`;
            }).join('');
        });

        // تحديث الدائرة
        const offset = 283 - (283 * d.safety / 100);
        document.getElementById('safetyRing').style.strokeDashoffset = offset;
        document.getElementById('safetyVal').innerText = d.safety + "%";

        // تحديث البار الأفقي
        const colors = ['#00f2ff', '#39ff14', '#ffea00', '#ff9100', '#ff0055', '#a020f0'];
        if(!chart) {
            const ctx = document.getElementById('horizChart').getContext('2d');
            chart = new Chart(ctx, {
                type: 'bar',
                data: { labels: d.groups.map(g => g.title), datasets: [{ data: d.groups.map(g => g.items[0][1] + 1), backgroundColor: colors, borderRadius: 5 }] },
                options: { indexAxis: 'y', maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { grid: { display: false }, ticks: { color: '#fff', font: { weight: 'bold', size: 9 } } } } }
            });
        } else {
            chart.data.datasets[0].data = d.groups.map(g => g.items[0][1] + 1);
            chart.update();
        }
        current = (current + 1) % clinicalDB.length;
    }

    init();
    setInterval(updateData, 15000);
</script>
</body>
</html>
"""

components.html(dashboard_html, height=950, scrolling=False)
