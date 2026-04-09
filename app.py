import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Riyadh | Executive View", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        :root {
            --bg: #020617;
            --card-bg: rgba(15, 23, 42, 0.95);
            --neon-blue: #22d3ee;
            --border-clr: rgba(255, 255, 255, 0.1);
            --text-main: #f8fafc;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0; padding: 20px; overflow: hidden;
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--card-bg); padding: 15px 40px;
            border-radius: 15px; border: 1px solid var(--border-clr);
            margin-bottom: 20px;
        }

        /* المربعات الكبيرة التي تحتوي على البيانات الفرعية */
        .main-layout {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 25px;
        }

        .mega-card {
            background: var(--card-bg);
            border: 2px solid var(--border-clr);
            border-radius: 20px;
            padding: 20px;
            min-height: 220px;
            transition: 0.3s;
        }

        .mega-card:hover { border-color: var(--neon-blue); }

        .mega-title {
            color: var(--neon-blue);
            font-weight: 900;
            font-size: 1.1rem;
            margin-bottom: 15px;
            border-bottom: 1px solid rgba(34, 211, 238, 0.2);
            padding-bottom: 10px;
        }

        .sub-data-row {
            display: flex; justify-content: space-between; margin-bottom: 10px;
        }

        .label { color: #94a3b8; font-size: 0.85rem; font-weight: 600; }
        .value { font-weight: 900; font-size: 1.2rem; }

        /* منطقة الدوائر المتغيرة */
        .safety-section {
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 20px;
            height: 300px;
        }

        .score-panel {
            background: var(--card-bg); border-radius: 20px;
            display: flex; justify-content: space-around; align-items: center;
            border: 1px solid var(--border-clr);
        }

        .circle-container { text-align: center; }

        .circle {
            width: 160px; height: 160px; border-radius: 50%;
            border: 10px solid #1e293b; display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            transition: 1s ease-in-out;
        }

        .circle-num { font-size: 3rem; font-weight: 900; }
        .circle-label { margin-top: 10px; font-weight: 800; color: #94a3b8; font-size: 0.8rem; }
    </style>
</head>
<body>
    <div class="header">
        <h1 style="margin:0; font-size:1.5rem;">ICU PERFORMANCE | <span id="qTag">4Q 2023</span></h1>
        <div style="font-weight:900; color:var(--neon-blue);">SAUDI GERMAN RIYADH</div>
    </div>

    <div class="main-layout" id="megaGrid"></div>

    <div class="safety-section">
        <div class="score-panel">
            <div class="circle-container">
                <div class="circle" id="ring1" style="border-color: #22d3ee;">
                    <div class="circle-num" id="score1">0%</div>
                </div>
                <div class="circle-label">UNIT SAFETY SCORE</div>
            </div>
            <div class="circle-container">
                <div class="circle" id="ring2" style="border-color: #34d399;">
                    <div class="circle-num" id="score2">0%</div>
                </div>
                <div class="circle-label">BSN EDUCATION</div>
            </div>
        </div>
        
        <div class="mega-card" style="display:flex; flex-direction:column; justify-content:center;">
            <div class="mega-title">MONTHLY HIGHLIGHTS</div>
            <div id="highlights">...</div>
        </div>
    </div>

    <script>
        const clinicalData = [
            { 
                q: "4Q 2023",
                safety: 88,
                bsn: 67,
                groups: [
                    { title: "Falls Metric", subs: [["Total Falls", 0], ["Injury Falls", 0], ["Benchmark", 0.04]] },
                    { title: "Pressure Injury", subs: [["HAPI Count", 7.3], ["Target", 26.6]] },
                    { title: "Infections", subs: [["CLABSI", 1.38], ["CAUTI", 0], ["VAE", 1.57]] }
                ]
            },
            { 
                q: "1Q 2024",
                safety: 75,
                bsn: 83,
                groups: [
                    { title: "Falls Metric", subs: [["Total Falls", 0.24], ["Injury Falls", 0.1], ["Benchmark", 0.09]] },
                    { title: "Pressure Injury", subs: [["HAPI Count", 6.45], ["Target", 7.77]] },
                    { title: "Infections", subs: [["CLABSI", 1.28], ["CAUTI", 0.70], ["VAE", 2.17]] }
                ]
            }
        ];

        let step = 0;

        function refresh() {
            const data = clinicalData[step];
            document.getElementById('qTag').innerText = data.q;
            
            // تحديث المربعات الكبيرة
            const grid = document.getElementById('megaGrid');
            grid.innerHTML = '';
            data.groups.forEach(g => {
                let rows = g.subs.map(s => `
                    <div class="sub-data-row">
                        <span class="label">${s[0]}</span>
                        <span class="value">${s[1]}</span>
                    </div>`).join('');
                
                grid.innerHTML += `
                    <div class="mega-card">
                        <div class="mega-title">${g.title}</div>
                        ${rows}
                    </div>`;
            });

            // تحديث الدوائر المتغيرة
            document.getElementById('score1').innerText = data.safety + "%";
            document.getElementById('score2').innerText = data.bsn + "%";
            
            step = (step + 1) % clinicalData.length;
        }

        refresh();
        setInterval(refresh, 20000);
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=850, scrolling=False)
