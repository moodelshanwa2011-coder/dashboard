import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Riyadh | Pro Dashboard", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #050a18;
            --card: rgba(16, 24, 48, 0.9);
            --neon: #00f2ff;
            --danger: #ff3131;
            --border: rgba(0, 242, 255, 0.15);
        }
        
        body {
            font-family: 'Segoe UI', Roboto, sans-serif;
            background: var(--bg); color: #fff; margin: 0; padding: 15px; overflow: hidden;
        }

        /* Header */
        .header {
            display: flex; justify-content: space-between; align-items: center;
            padding: 10px 30px; background: var(--card); border: 1px solid var(--border);
            border-radius: 12px; margin-bottom: 15px; box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }

        /* Layout العضوي - المربعات ليست متساوية */
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-auto-rows: minmax(180px, auto);
            gap: 15px;
        }

        .container {
            background: var(--card); border: 1px solid var(--border);
            border-radius: 16px; padding: 15px; position: relative;
            transition: 0.3s;
        }

        /* جعل بعض المربعات أكبر من غيرها */
        .large { grid-column: span 2; } 
        .tall { grid-row: span 2; }

        .title {
            font-size: 0.8rem; font-weight: 800; color: var(--neon);
            text-transform: uppercase; letter-spacing: 1px;
            margin-bottom: 15px; border-left: 3px solid var(--neon); padding-left: 10px;
        }

        /* المربعات الرقمية بدلاً من الدوائر */
        .tiles-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); gap: 10px; }
        
        .tile {
            background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05);
            border-radius: 10px; padding: 10px; text-align: center;
        }

        .tile-val { font-size: 1.6rem; font-weight: 900; display: block; transition: 0.5s; }
        .tile-label { font-size: 0.6rem; color: #8492a6; font-weight: bold; margin-top: 4px; display: block;}
        .tile-bm { font-size: 0.55rem; color: #475569; display: block; margin-top: 2px;}

        .safe { color: var(--neon); text-shadow: 0 0 10px rgba(0, 242, 255, 0.3); }
        .warn { color: var(--danger); text-shadow: 0 0 10px rgba(255, 49, 49, 0.3); }

        /* Music Visualizer Chart */
        .visualizer-container {
            margin-top: 15px; background: var(--card); border-radius: 16px;
            padding: 15px; height: 220px; border: 1px solid var(--border);
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h2 style="margin:0; font-size:1.1rem; letter-spacing:1px;">ICU RIYADH <span style="color:var(--neon)">| CLINICAL PERFORMANCE</span></h2>
        </div>
        <div style="background:var(--neon); color:#000; padding:5px 20px; border-radius:8px; font-weight:900;" id="qText">Q-DATA</div>
    </div>

    <div class="dashboard-grid" id="mainGrid"></div>

    <div class="visualizer-container">
        <canvas id="musicChart"></canvas>
    </div>

    <script>
        const clinicalData = [
            {
                q: "4Q 2023",
                groups: [
                    { title: "Falls Analysis", size: "normal", items: [["Total", 0, 0.04], ["Injury", 0, 0.03]] },
                    { title: "Pressure Injury (HAPI)", size: "normal", items: [["Stage 2+", 7.3, 26.6], ["Unit Acq", 0, 0]] },
                    { title: "Device Infections", size: "large", items: [["CLABSI", 1.38, 1.3], ["CAUTI", 0, 0.46], ["VAE", 1.57, 1.06], ["VAP", 0, 0]] },
                    { title: "Microbiology", size: "normal", items: [["MDRO", 0, 0], ["C-Diff", 0, 0]] },
                    { title: "Nursing Workforce", size: "large", items: [["BSN %", 67.2, 83.5], ["Turnover", 5.21, 1.6], ["RN Hours", 13.0, 8.0], ["CNA Hours", 1.1, 1.2]] },
                    { title: "Patient Restraints", size: "normal", items: [["Physical", 23.3, 5.08]] },
                    { title: "Safety Summary", size: "normal", items: [["Unit Safety", 88, 75]] }
                ]
            },
            {
                q: "1Q 2024",
                groups: [
                    { title: "Falls Analysis", size: "normal", items: [["Total", 0.24, 0.09], ["Injury", 0.1, 0.04]] },
                    { title: "Pressure Injury (HAPI)", size: "normal", items: [["Stage 2+", 6.45, 7.7], ["Unit Acq", 0, 0]] },
                    { title: "Device Infections", size: "large", items: [["CLABSI", 1.28, 2.67], ["CAUTI", 0.7, 0.99], ["VAE", 2.17, 2.42], ["VAP", 0.2, 0]] },
                    { title: "Microbiology", size: "normal", items: [["MDRO", 0.21, 0], ["C-Diff", 0.15, 0]] },
                    { title: "Nursing Workforce", size: "large", items: [["BSN %", 83.0, 70.3], ["Turnover", 4.84, 4.49], ["RN Hours", 20.1, 19.1], ["CNA Hours", 1.5, 1.3]] },
                    { title: "Patient Restraints", size: "normal", items: [["Physical", 6.45, 6.47]] },
                    { title: "Safety Summary", size: "normal", items: [["Unit Safety", 92, 75]] }
                ]
            }
        ];

        let step = 0;
        let mChart;

        function update() {
            const data = clinicalData[step];
            document.getElementById('qText').innerText = data.q;
            const grid = document.getElementById('mainGrid');
            grid.innerHTML = '';

            data.groups.forEach(g => {
                let tiles = g.items.map(i => {
                    const isSafe = (i[0].includes("%") || i[0].includes("Hours")) ? (i[1] >= i[2]) : (i[1] <= i[2]);
                    return `
                        <div class="tile">
                            <span class="tile-val ${isSafe?'safe':'warn'}">${i[1]}</span>
                            <span class="tile-label">${i[0]}</span>
                            <span class="tile-bm">BM: ${i[2]}</span>
                        </div>`;
                }).join('');

                grid.innerHTML += `
                    <div class="container ${g.size}">
                        <div class="title">${g.title}</div>
                        <div class="tiles-grid">${tiles}</div>
                    </div>`;
            });

            // تحديث أعمدة الموسيقى (Visualizer)
            const chartData = data.groups.map(g => g.items[0][1]);
            if(!mChart) {
                const ctx = document.getElementById('musicChart').getContext('2d');
                mChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.groups.map(g => g.title),
                        datasets: [{ data: chartData, backgroundColor: '#00f2ff', borderRadius: 5 }]
                    },
                    options: {
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        animation: { duration: 1500, easing: 'easeInOutElastic' }, // حركة "موسيقية" مطاطية
                        scales: { y: { display: false }, x: { ticks: { color: '#8492a6', font: { size: 9 } } } }
                    }
                });
            } else {
                mChart.data.datasets[0].data = chartData;
                mChart.update();
            }

            step = (step + 1) % clinicalData.length;
        }

        update();
        setInterval(update, 20000);
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=950, scrolling=False)
