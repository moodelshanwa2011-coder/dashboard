import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Riyadh | Grouped KPIs", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        :root {
            --bg: #020617;
            --card-bg: rgba(15, 23, 42, 0.9);
            --neon-blue: #22d3ee;
            --neon-green: #34d399;
            --neon-red: #f43f5e;
            --border-clr: rgba(255, 255, 255, 0.15);
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
            margin-bottom: 25px;
        }

        /* حاوية المربعات الكبيرة */
        .main-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
            margin-bottom: 25px;
        }

        .parent-card {
            background: var(--card-bg);
            border: 2px solid var(--border-clr);
            border-radius: 25px;
            padding: 20px;
            position: relative;
        }

        .parent-title {
            position: absolute; top: -15px; left: 30px;
            background: var(--neon-blue); color: #020617;
            padding: 5px 20px; border-radius: 10px;
            font-weight: 900; font-size: 0.9rem; text-transform: uppercase;
        }

        .sub-grid {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 15px;
        }

        .sub-item {
            background: rgba(255,255,255,0.03);
            padding: 15px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.05);
            text-align: center;
        }

        .sub-val { font-size: 1.8rem; font-weight: 800; display: block; }
        .sub-label { font-size: 0.7rem; color: #94a3b8; font-weight: bold; }
        .sub-bm { font-size: 0.6rem; color: #475569; display: block; margin-top: 5px; }

        /* دائرة الـ Safety Score الكبيرة */
        .footer-section {
            display: flex; justify-content: center; align-items: center;
            background: var(--card-bg); border-radius: 25px; padding: 30px;
            border: 1px solid var(--border-clr); height: 250px;
        }

        .score-circle {
            width: 180px; height: 180px; border-radius: 50%;
            border: 12px solid #1e293b; display: flex; flex-direction: column;
            align-items: center; justify-content: center; position: relative;
            box-shadow: 0 0 30px rgba(34, 211, 238, 0.2);
        }

        .score-num { font-size: 3.5rem; font-weight: 900; }
        .safe { color: var(--neon-blue); }
        .alert { color: var(--neon-red); }
    </style>
</head>
<body>
    <div class="header">
        <h1 style="margin:0; font-size:1.5rem;">ICU PERFORMANCE <span style="color:var(--neon-blue)">GROUPED VIEW</span></h1>
        <div style="background:#1e293b; padding:10px 25px; border-radius:12px; font-weight:900;" id="qDisplay">...</div>
    </div>

    <div class="main-grid" id="mainGrid"></div>

    <div class="footer-section">
        <div style="text-align:center; margin-right:50px;">
            <h2 style="margin:0; font-size:1.2rem; color:var(--neon-blue);">UNIT SAFETY SCORE</h2>
            <p style="color:#64748b; font-size:0.8rem;">Calculated based on Clinical Targets</p>
        </div>
        <div class="score-circle" id="mainRing">
            <div class="score-num" id="safetyScore">0%</div>
        </div>
    </div>

    <script>
        const clinicalData = [
            { 
                q: "4Q 2023",
                groups: [
                    { title: "Patient Safety", items: ["Falls", "HAPI"], vals: [0, 7.30], bms: [0.04, 26.67] },
                    { title: "Device Infections", items: ["CLABSI", "CAUTI"], vals: [1.38, 0], bms: [1.3, 0.46] },
                    { title: "Respiratory", items: ["VAE", "VAP"], vals: [1.57, 0], bms: [1.06, 0] },
                    { title: "Staffing Metrics", items: ["Turnover", "BSN %"], vals: [5.21, 67.2], bms: [1.6, 83.5] }
                ]
            },
            { 
                q: "1Q 2024",
                groups: [
                    { title: "Patient Safety", items: ["Falls", "HAPI"], vals: [0.24, 6.45], bms: [0.09, 7.77] },
                    { title: "Device Infections", items: ["CLABSI", "CAUTI"], vals: [1.28, 0.70], bms: [2.67, 0.99] },
                    { title: "Respiratory", items: ["VAE", "VAP"], vals: [2.17, 0], bms: [2.42, 0] },
                    { title: "Staffing Metrics", items: ["Turnover", "BSN %"], vals: [4.84, 83.0], bms: [4.49, 70.3] }
                ]
            }
            // يمكن إضافة باقي الأرباع هنا بنفس النسق
        ];

        let step = 0;

        function update() {
            const data = clinicalData[step];
            document.getElementById('qDisplay').innerText = data.q;
            
            const grid = document.getElementById('mainGrid');
            grid.innerHTML = '';
            
            let totalItems = 0;
            let metTargets = 0;

            data.groups.forEach(group => {
                let itemsHtml = '';
                group.items.forEach((name, i) => {
                    totalItems++;
                    const val = group.vals[i];
                    const bm = group.bms[i];
                    
                    // منطق الحساب: إذا كان المؤشر (Infection/Fall) أقل من الـ Benchmark فهو آمن
                    const isSafe = (name === "BSN %") ? (val >= bm) : (val <= bm);
                    if(isSafe) metTargets++;

                    itemsHtml += `
                        <div class="sub-item">
                            <span class="sub-label">${name}</span>
                            <span class="sub-val ${isSafe?'safe':'alert'}">${val}</span>
                            <span class="sub-bm">Target: ${bm}</span>
                        </div>`;
                });

                grid.innerHTML += `
                    <div class="parent-card">
                        <div class="parent-title">${group.title}</div>
                        <div class="sub-grid">${itemsHtml}</div>
                    </div>`;
            });

            // حساب الـ Unit Safety Score
            const score = Math.round((metTargets / totalItems) * 100);
            const scoreEl = document.getElementById('safetyScore');
            const ring = document.getElementById('mainRing');
            
            scoreEl.innerText = score + "%";
            const color = score >= 75 ? "#22d3ee" : "#f43f5e";
            scoreEl.style.color = color;
            ring.style.borderColor = color;

            step = (step + 1) % clinicalData.length;
        }

        update();
        setInterval(update, 20000);
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=900, scrolling=False)
