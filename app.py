import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ICU Riyadh | Pro Intelligence",
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
            --bg: #020617;
            --card-bg: rgba(15, 23, 42, 0.8);
            --neon-blue: #00f2ff;
            --danger: #ff0055;
            --border: rgba(0, 242, 255, 0.2);
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg);
            color: #fff; margin: 0; padding: 15px; overflow: hidden;
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 10px 25px; background: var(--card-bg); border-radius: 12px;
            border: 1px solid var(--border); margin-bottom: 15px;
        }

        .dashboard-grid {
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 12px; margin-bottom: 15px;
        }

        .mega-card {
            background: var(--card-bg); border: 1.5px solid var(--border);
            border-radius: 16px; padding: 15px; backdrop-filter: blur(10px);
            transition: 0.4s;
        }
        .mega-card:hover { border-color: var(--neon-blue); box-shadow: 0 0 15px rgba(0, 242, 255, 0.2); }

        .span-2 { grid-column: span 2; }

        .title {
            font-size: 0.75rem; font-weight: 900; color: var(--neon-blue);
            text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;
            border-left: 3px solid var(--neon-blue); padding-left: 8px;
        }

        .tiles-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 10px; }
        
        .tile {
            background: rgba(255,255,255,0.02); border-radius: 10px;
            padding: 10px; text-align: center; border: 1px solid rgba(255,255,255,0.05);
        }

        .tile-val { font-size: 1.6rem; font-weight: 900; display: block; transition: color 0.5s ease; }
        .tile-label { font-size: 0.6rem; color: #94a3b8; text-transform: uppercase; margin-top: 5px; font-weight: bold; }
        
        /* إظهار كلمة Benchmark كاملة */
        .tile-bm { font-size: 0.6rem; color: #475569; display: block; margin-top: 4px; font-weight: 600; }

        .footer-row { display: grid; grid-template-columns: 2.8fr 1.2fr; gap: 12px; height: 200px; }

        .safe { color: var(--neon-blue); text-shadow: 0 0 8px rgba(0, 242, 255, 0.4); }
        .warn { color: var(--danger); text-shadow: 0 0 8px rgba(255, 0, 85, 0.4); }

        .safety-box { display: flex; align-items: center; justify-content: space-around; position: relative; }
        .ring-text { position: absolute; font-size: 1.8rem; font-weight: 900; color: var(--neon-blue); left: 33px; top: 75px;}
    </style>
</head>
<body>
    <div class="header">
        <h2 style="margin:0; font-size:1rem; letter-spacing:1px;">SGH RIYADH | ICU <span style="color:var(--neon-blue)">DASHBOARD</span></h2>
        <div id="qLabel" style="border: 1px solid var(--neon-blue); color: var(--neon-blue); padding: 3px 15px; border-radius: 6px; font-weight: 900;">...</div>
    </div>

    <div class="dashboard-grid" id="mainGrid"></div>

    <div class="footer-row">
        <div class="mega-card" style="padding:10px;">
            <canvas id="barChart"></canvas>
        </div>
        <div class="mega-card safety-box">
            <div style="position:relative; width:120px; height:120px;">
                <svg viewBox="0 0 100 100" style="transform: rotate(-90deg); width:120px;">
                    <circle cx="50" cy="50" r="45" fill="none" stroke="#161b22" stroke-width="8"></circle>
                    <circle id="ring" cx="50" cy="50" r="45" fill="none" stroke="#00f2ff" stroke-width="8" 
                            stroke-dasharray="283" stroke-dashoffset="283" stroke-linecap="round" style="transition: 1.5s;"></circle>
                </svg>
                <div id="safetyScore" style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:1.6rem; font-weight:900; color:#00f2ff;">0%</div>
            </div>
            <div style="text-align:left; padding-left:15px;">
                <div style="font-size:0.7rem; color:#94a3b8; font-weight:bold;">UNIT SAFETY PERCENT</div>
                <div style="font-size:0.55rem; color:#475569; margin-top:4px;">Calculated based on clinical benchmarks</div>
            </div>
        </div>
    </div>

    <script>
        const clinicalDB = [
            {
                q: "4Q 2023", safety: 88,
                groups: [
                    { title: "Falls Analysis", class: "", items: [["Total Falls", 0, 0.04], ["Injury Falls", 0, 0.03]] },
                    { title: "Infections (Device)", class: "span-2", items: [["CLABSI", 1.38, 1.30], ["CAUTI", 0, 0.46], ["VAE", 1.57, 1.06], ["VAP", 0, 0]] },
                    { title: "Pressure Injury", class: "", items: [["Survey %", 7.3, 26.6], ["Unit Acq", 0, 0]] },
                    { title: "Workforce", class: "span-2", items: [["BSN %", 67.2, 83.5], ["Turnover", 5.21, 1.6], ["RN Hours", 13.0, 8.0], ["CNA Hours", 1.1, 1.2]] },
                    { title: "Safety & MDRO", class: "", items: [["Restraints", 23.3, 5.08], ["MDRO-MRSA", 0.21, 0]] }
                ]
            },
            {
                q: "1Q 2024", safety: 92,
                groups: [
                    { title: "Falls Analysis", class: "", items: [["Total Falls", 0.24, 0.09], ["Injury Falls", 0, 0.04]] },
                    { title: "Infections (Device)", class: "span-2", items: [["CLABSI", 1.28, 2.67], ["CAUTI", 0.70, 0.99], ["VAE", 2.17, 2.42], ["VAP", 0, 0]] },
                    { title: "Pressure Injury", class: "", items: [["Survey %", 6.45, 7.77], ["Unit Acq", 0, 0]] },
                    { title: "Workforce", class: "span-2", items: [["BSN %", 83.0, 70.3], ["Turnover", 4.84, 4.49], ["RN Hours", 20.1, 19.1], ["CNA Hours", 1.5, 1.3]] },
                    { title: "Safety & MDRO", class: "", items: [["Restraints", 6.45, 6.47], ["MDRO-MRSA", 0.22, 0]] }
                ]
            }
        ];

        let idx = 0;
        let chart;

        function refresh() {
            const data = clinicalDB[idx];
            document.getElementById('qLabel').innerText = data.q;
            const grid = document.getElementById('mainGrid');
            grid.innerHTML = '';

            data.groups.forEach(g => {
                let tiles = g.items.map(i => {
                    const isSafe = (i[0].includes("BSN") || i[0].includes("Hours")) ? (i[1] >= i[2]) : (i[1] <= i[2]);
                    return `
                        <div class="tile">
                            <span class="tile-val ${isSafe?'safe':'warn'}">${i[1]}</span>
                            <span class="tile-label">${i[0]}</span>
                            <span class="tile-bm">Benchmark: ${i[2]}</span>
                        </div>`;
                }).join('');
                grid.innerHTML += `<div class="mega-card ${g.class}"><div class="title">${g.title}</div><div class="tiles-grid">${tiles}</div></div>`;
            });

            // Update Ring
            const offset = 283 - (283 * data.safety / 100);
            document.getElementById('ring').style.strokeDashoffset = offset;
            document.getElementById('safetyScore').innerText = data.safety + "%";

            // Update Music Bar (Pro Visualizer)
            const bVals = data.groups.map(g => g.items[0][1]);
            if(!chart) {
                const ctx = document.getElementById('barChart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'bar',
                    data: { labels: data.groups.map(g => g.title), datasets: [{ data: bVals, backgroundColor: '#00f2ff' }] },
                    options: { 
                        maintainAspectRatio: false, animation: { duration: 1500, easing: 'easeInOutQuart' },
                        plugins: { legend: { display: false } },
                        scales: { x: { grid: { display: false }, ticks: { color: '#475569', font: { size: 9 } } }, y: { display: false } },
                        categoryPercentage: 1.0, barPercentage: 0.95
                    }
                });
            } else {
                chart.data.datasets[0].data = bVals;
                chart.update();
            }
            idx = (idx + 1) % clinicalDB.length;
        }

        refresh();
        setInterval(refresh, 15000); // 15 Seconds
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=880, scrolling=False)
