import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Performance | SGH", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #010409;
            --panel-bg: rgba(13, 17, 23, 0.85);
            --neon: #00f2ff;
            --grid-color: rgba(0, 242, 255, 0.15); /* حدود الشبكة في الخلفية */
            --border-panel: rgba(0, 242, 255, 0.4);
        }
        
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: var(--bg);
            /* الشبكة الهندسية واضحة جداً */
            background-image: 
                linear-gradient(var(--grid-color) 1px, transparent 1px),
                linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
            background-size: 40px 40px;
            color: #fff; margin: 0; padding: 20px; overflow: hidden;
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--panel-bg); padding: 12px 25px; border-radius: 12px;
            border: 2px solid var(--border-panel); margin-bottom: 20px;
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
        }

        .dashboard-main {
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 20px; margin-bottom: 20px;
        }

        .panel {
            background: var(--panel-bg); border: 2px solid var(--border-panel);
            border-radius: 15px; padding: 20px; backdrop-filter: blur(8px);
        }

        .span-2 { grid-column: span 2; }

        .panel-title {
            font-size: 0.85rem; font-weight: 800; color: var(--neon);
            text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 15px;
            display: flex; align-items: center; gap: 8px;
        }

        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; }
        
        .stat-box {
            background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
            border-radius: 10px; padding: 12px; text-align: center;
        }

        .val { font-size: 1.8rem; font-weight: 900; display: block; }
        .lbl { font-size: 0.65rem; color: #8b949e; text-transform: uppercase; font-weight: bold; margin-top: 5px; }
        .benchmark { font-size: 0.65rem; color: #484f58; display: block; margin-top: 5px; font-weight: bold; }

        .safe { color: var(--neon); }
        .warn { color: #ff0055; }

        .footer { display: grid; grid-template-columns: 2.5fr 1.5fr; gap: 20px; height: 280px; }

        .chart-panel { position: relative; padding: 15px; }
        
        .safety-index { display: flex; align-items: center; justify-content: space-around; }
        .ring-container { position: relative; width: 140px; height: 140px; }
        .ring-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 1.8rem; font-weight: 900; color: var(--neon); }
    </style>
</head>
<body>

<div class="header">
    <div style="font-size: 1.2rem; font-weight: 900;">SGH RIYADH <span style="color:var(--neon)">| ICU INTELLIGENCE</span></div>
    <div id="qLabel" style="border: 2px solid var(--neon); color: var(--neon); padding: 4px 20px; border-radius: 6px; font-weight: 900;">...</div>
</div>

<div class="dashboard-main" id="mainGrid"></div>

<div class="footer">
    <div class="panel chart-panel">
        <canvas id="horizChart"></canvas>
    </div>
    
    <div class="panel safety-index">
        <div class="ring-container">
            <svg viewBox="0 0 100 100" style="transform: rotate(-90deg);">
                <circle cx="50" cy="50" r="45" fill="none" stroke="#161b22" stroke-width="8"></circle>
                <circle id="safetyRing" cx="50" cy="50" r="45" fill="none" stroke="#00f2ff" stroke-width="8" 
                        stroke-dasharray="283" stroke-dashoffset="283" stroke-linecap="round" style="transition: 1.5s;"></circle>
            </svg>
            <div id="safetyVal" class="ring-text">0%</div>
        </div>
        <div style="text-align: left;">
            <div style="font-size: 0.8rem; font-weight: 900; color: #8b949e;">COMPLIANCE SCORE</div>
            <div style="font-size: 0.6rem; color: #484f58; margin-top: 4px;">BASED ON BENCHMARK DATA</div>
        </div>
    </div>
</div>

<script>
    const clinicalData = [
        {
            q: "4Q 2023", safety: 88,
            groups: [
                { title: "Falls Analysis", class: "", items: [["Total Falls", 0, 0.04], ["Injury Falls", 0, 0.03]] },
                { title: "Device Infections", class: "span-2", items: [["CLABSI", 1.38, 1.30], ["CAUTI", 0, 0.46], ["VAE", 1.57, 1.06]] },
                { title: "Staffing Metrics", class: "", items: [["BSN %", 67.2, 83.5], ["Turnover", 5.21, 1.6]] }
            ]
        },
        {
            q: "1Q 2024", safety: 92,
            groups: [
                { title: "Falls Analysis", class: "", items: [["Total Falls", 0.24, 0.09], ["Injury Falls", 0, 0.04]] },
                { title: "Device Infections", class: "span-2", items: [["CLABSI", 1.28, 2.67], ["CAUTI", 0.70, 0.99], ["VAE", 2.17, 2.42]] },
                { title: "Staffing Metrics", class: "", items: [["BSN %", 83.0, 70.3], ["Turnover", 4.84, 4.49]] }
            ]
        }
    ];

    let idx = 0;
    let chartInstance;

    function refresh() {
        const d = clinicalData[idx];
        document.getElementById('qLabel').innerText = d.q;
        
        const grid = document.getElementById('mainGrid');
        grid.innerHTML = '';
        d.groups.forEach(g => {
            let tiles = g.items.map(i => {
                const isSafe = (i[0].includes("BSN")) ? (i[1] >= i[2]) : (i[1] <= i[2]);
                return `<div class="stat-box">
                    <span class="val ${isSafe?'safe':'warn'}">${i[1]}</span>
                    <span class="lbl">${i[0]}</span>
                    <span class="benchmark">Benchmark: ${i[2]}</span>
                </div>`;
            }).join('');
            grid.innerHTML += `<div class="panel ${g.class}"><div class="panel-title">${g.title}</div><div class="stats-grid">${tiles}</div></div>`;
        });

        document.getElementById('safetyRing').style.strokeDashoffset = 283 - (283 * d.safety / 100);
        document.getElementById('safetyVal').innerText = d.safety + "%";

        // ألوان مختلفة لكل عمود
        const colors = ['#00f2ff', '#39ff14', '#ff0055', '#ffea00'];
        const barLabels = d.groups.map(g => g.title);
        const barVals = d.groups.map(g => g.items[0][1] + 1);

        if(!chartInstance) {
            const ctx = document.getElementById('horizChart').getContext('2d');
            chartInstance = new Chart(ctx, {
                type: 'bar',
                data: { labels: barLabels, datasets: [{ data: barVals, backgroundColor: colors, borderRadius: 5, barThickness: 20 }] },
                options: {
                    indexAxis: 'y',
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { display: false },
                        y: { grid: { display: false }, ticks: { color: '#fff', font: { weight: 'bold', size: 10 } } }
                    }
                }
            });
        } else {
            chartInstance.data.datasets[0].data = barVals;
            chartInstance.update();
        }
        idx = (idx + 1) % clinicalData.length;
    }

    refresh();
    setInterval(refresh, 15000);
</script>
</body>
</html>
"""

components.html(dashboard_html, height=950, scrolling=False)
