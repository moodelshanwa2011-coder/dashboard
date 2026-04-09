import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="SGH Riyadh | ICU Command Center",
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
            --card-bg: rgba(13, 17, 23, 0.98);
            --neon-blue: #00f2ff;
            --danger: #ff0055;
            --border: rgba(0, 242, 255, 0.4);
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: #fff; margin: 0; padding: 10px; overflow: hidden;
        }

        /* الهيدر الاحترافي */
        .header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 12px 25px; background: var(--card-bg); border-radius: 12px;
            border: 2px solid var(--border); margin-bottom: 12px;
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
        }

        /* توزيع المربعات */
        .dashboard-grid {
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 12px; margin-bottom: 12px;
        }

        .mega-card {
            background: var(--card-bg); border: 2.5px solid var(--border);
            border-radius: 16px; padding: 18px; backdrop-filter: blur(15px);
            transition: 0.3s;
        }
        .mega-card:hover { border-color: var(--neon-blue); box-shadow: 0 0 20px rgba(0, 242, 255, 0.2); }

        .span-2 { grid-column: span 2; }

        .category-title {
            font-size: 0.85rem; font-weight: 900; color: var(--neon-blue);
            text-transform: uppercase; letter-spacing: 2px; margin-bottom: 15px;
            border-left: 5px solid var(--neon-blue); padding-left: 12px;
        }

        /* المربعات الرقمية */
        .tiles-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; }
        
        .tile {
            background: rgba(255,255,255,0.04); border-radius: 12px;
            padding: 15px; text-align: center; border: 1px solid rgba(255,255,255,0.08);
        }

        .tile-val { font-size: 2rem; font-weight: 900; display: block; line-height: 1; }
        .tile-label { font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; margin-top: 8px; font-weight: 800; }
        
        /* كلمة Benchmark كاملة وواضحة */
        .tile-bm { font-size: 0.65rem; color: #64748b; display: block; margin-top: 6px; font-weight: bold; letter-spacing: 0.5px; }

        .safe { color: var(--neon-blue); text-shadow: 0 0 12px rgba(0, 242, 255, 0.6); }
        .warn { color: var(--danger); text-shadow: 0 0 12px rgba(255, 0, 85, 0.6); }

        /* الفوتر: البار تشارت + الدائرة */
        .footer-row { display: grid; grid-template-columns: 2.8fr 1.2fr; gap: 12px; height: 230px; }

        .safety-box { display: flex; align-items: center; justify-content: center; gap: 20px; }
        
        .ring-container { position: relative; width: 140px; height: 140px; }
        .ring-text {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            font-size: 1.8rem; font-weight: 900; color: var(--neon-blue);
        }
    </style>
</head>
<body>
    <div class="header">
        <h2 style="margin:0; font-size:1.2rem; letter-spacing:2px;">SGH RIYADH | ICU <span style="color:var(--neon-blue)">COMMAND CENTER</span></h2>
        <div id="qLabel" style="background: var(--neon-blue); color: #000; padding: 5px 25px; border-radius: 8px; font-weight: 900; font-size: 1rem;">...</div>
    </div>

    <div class="dashboard-grid" id="mainGrid"></div>

    <div class="footer-row">
        <div class="mega-card" style="padding: 10px 10px 5px 10px;">
            <canvas id="proBarChart"></canvas>
        </div>
        
        <div class="mega-card safety-box">
            <div class="ring-container">
                <svg viewBox="0 0 100 100" style="transform: rotate(-90deg);">
                    <circle cx="50" cy="50" r="45" fill="none" stroke="#1e293b" stroke-width="10"></circle>
                    <circle id="ring" cx="50" cy="50" r="45" fill="none" stroke="#00f2ff" stroke-width="10" 
                            stroke-dasharray="283" stroke-dashoffset="283" stroke-linecap="butt" style="transition: 1.5s cubic-bezier(0.4, 0, 0.2, 1);"></circle>
                </svg>
                <div id="safetyScore" class="ring-text">0%</div>
            </div>
            <div style="text-align:left;">
                <div style="font-size:0.9rem; color:#94a3b8; font-weight:bold; letter-spacing:1px;">SAFETY INDEX</div>
                <div style="font-size:0.6rem; color:#475569; margin-top:5px; max-width:130px; font-weight: 600;">LIVE UNIT PERFORMANCE SCORE</div>
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
                    { title: "Workforce & Staffing", class: "span-2", items: [["BSN %", 67.2, 83.5], ["Turnover", 5.21, 1.6], ["RN Hours", 13.0, 8.0], ["CNA Hours", 1.1, 1.2]] },
                    { title: "Other Metrics", class: "", items: [["Restraints", 23.3, 5.08], ["MDRO-MRSA", 0.21, 0]] }
                ]
            },
            {
                q: "1Q 2024", safety: 92,
                groups: [
                    { title: "Falls Analysis", class: "", items: [["Total Falls", 0.24, 0.09], ["Injury Falls", 0, 0.04]] },
                    { title: "Device Infections", class: "span-2", items: [["CLABSI", 1.28, 2.67], ["CAUTI", 0.70, 0.99], ["VAE", 2.17, 2.42], ["VAP", 0, 0]] },
                    { title: "Workforce & Staffing", class: "span-2", items: [["BSN %", 83.0, 70.3], ["Turnover", 4.84, 4.49], ["RN Hours", 20.1, 19.1], ["CNA Hours", 1.5, 1.3]] },
                    { title: "Other Metrics", class: "", items: [["Restraints", 6.45, 6.47], ["MDRO-MRSA", 0.22, 0]] }
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
                grid.innerHTML += `<div class="mega-card ${g.class}"><div class="category-title">${g.title}</div><div class="tiles-grid">${tiles}</div></div>`;
            });

            // تحديث الدائرة
            document.getElementById('ring').style.strokeDashoffset = 283 - (283 * data.safety / 100);
            document.getElementById('safetyScore').innerText = data.safety + "%";

            // تحديث البار تشارت (أعمدة عريضة ومسطحة كما في الصورة)
            const bVals = data.groups.map(g => g.items[0][1] + 1.5);
            if(!chart) {
                const ctx = document.getElementById('proBarChart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'bar',
                    data: { 
                        labels: data.groups.map(g => g.title), 
                        datasets: [{ 
                            data: bVals, 
                            backgroundColor: '#00f2ff',
                            borderRadius: 0, 
                            borderSkipped: false
                        }] 
                    },
                    options: { 
                        maintainAspectRatio: false, 
                        animation: { duration: 1500, easing: 'easeInOutQuart' },
                        plugins: { legend: { display: false } },
                        scales: { 
                            x: { grid: { display: false }, ticks: { color: '#8b949e', font: { size: 10, weight: 'bold' } } }, 
                            y: { display: false } 
                        },
                        categoryPercentage: 1.0, 
                        barPercentage: 0.95 // تلاصق الأعمدة وضخامتها
                    }
                });
            } else {
                chart.data.datasets[0].data = bVals;
                chart.update();
            }
            idx = (idx + 1) % clinicalDB.length;
        }

        refresh();
        setInterval(refresh, 15000); 
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=920, scrolling=False)
