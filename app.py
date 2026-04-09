import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ICU Riyadh | Medical Device Census",
    layout="wide",
    initial_sidebar_state="collapsed"
)

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        :root {
            --bg: #010409;
            --card-top: rgba(23, 32, 42, 0.9);
            --card-bottom: rgba(30, 41, 59, 0.5);
            --neon-blue: #00f2ff;
            --neon-green: #39ff14;
            --neon-red: #ff3131;
            --text-main: #e6edf3;
        }
        
        body {
            font-family: 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0; padding: 20px; overflow: hidden;
        }

        /* Header Style */
        .header {
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 2px solid rgba(0, 242, 255, 0.2);
            padding-bottom: 15px; margin-bottom: 20px;
        }

        /* تصميم المربعات العلوية - نمط البطاقات الزجاجية الدائرية */
        .top-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        
        .top-card {
            background: var(--card-top);
            border-radius: 50px 5px 50px 5px; /* شكل مختلف ومميز */
            padding: 20px; text-align: center;
            border: 1px solid rgba(0, 242, 255, 0.3);
            box-shadow: inset 0 0 15px rgba(0, 242, 255, 0.1);
        }

        .top-val { font-size: 3rem; font-weight: 900; margin: 5px 0; }
        .top-label { font-size: 0.8rem; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; }

        /* تصميم القسم السفلي - نمط المصفوفة التقنية */
        .census-container {
            background: var(--card-bottom);
            border-radius: 20px; padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            height: 450px;
        }

        .census-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr); /* 5 أعمدة كما في الصور */
            gap: 15px; height: 85%;
        }

        .column-box {
            background: rgba(0, 0, 0, 0.3);
            border: 1px dashed rgba(255, 255, 255, 0.1);
            border-radius: 12px; padding: 15px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            position: relative;
        }

        .column-val { font-size: 2.2rem; font-weight: 800; color: var(--neon-green); }
        .column-sub { font-size: 0.7rem; color: #484f58; margin-top: 5px; text-align: center;}

        /* أعمدة الموسيقى (Music Visualizer) */
        .visualizer {
            display: flex; align-items: flex-end; gap: 4px; height: 40px; margin-top: 15px;
        }
        .bar {
            width: 5px; background: var(--neon-green); border-radius: 10px;
            animation: pulse 1.2s infinite ease-in-out;
        }
        @keyframes pulse {
            0%, 100% { height: 10px; opacity: 0.4; }
            50% { height: 35px; opacity: 1; filter: brightness(1.2); }
        }

        .safe { color: var(--neon-blue); }
        .alert { color: var(--neon-red); }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1 style="margin:0; font-size:1.6rem;">SAUDI GERMAN HOSPITAL <span style="color:var(--neon-blue)">| ICU CENSUS</span></h1>
            <p id="timeLabel" style="color:#8b949e; font-size:0.9rem; font-weight:bold; margin-top:5px;">LIVE DATA TRACKING</p>
        </div>
        <div style="text-align:right">
            <div style="font-size:1.2rem; font-weight:900; color:var(--neon-blue)" id="periodText">MARCH 2026</div>
            <div style="font-size:0.7rem; opacity:0.5">REFRESH RATE: 20s</div>
        </div>
    </div>

    <div class="top-grid" id="topGrid"></div>

    <div class="census-container">
        <h2 style="font-size:1rem; margin-top:0; color:var(--neon-blue); letter-spacing:2px">WEEKLY DEVICE UTILIZATION</h2>
        <div class="census-grid" id="censusGrid"></div>
    </div>

    <script>
        // داتا الصور: Patient Stay, Foley, Central Line, Ventilator, IV Sites
        const dataset = [
            { 
                label: "MARCH - WEEK 1",
                top: [34, 14, 7, 14], // Patient Stay, Foley, Lines, Vent
                census: [34, 14, 7, 14, 25], // الـ 5 أعمدة من الصورة
                staff: "SAJEESH / VIMAL"
            },
            { 
                label: "MARCH - WEEK 2",
                top: [24, 15, 3, 11],
                census: [24, 15, 3, 11, 24],
                staff: "RINSON / NIKHIL"
            },
            { 
                label: "APRIL - WEEK 1",
                top: [29, 15, 8, 11],
                census: [29, 15, 8, 11, 22],
                staff: "JILS / VIMAL"
            },
            { 
                label: "APRIL - WEEK 2",
                top: [31, 18, 7, 12],
                census: [31, 18, 7, 12, 30],
                staff: "JILS / KHALED"
            }
        ];

        const topTitles = ["Total Stay", "Foley Catheter", "Central Lines", "Ventilators"];
        let currentIndex = 0;

        function refreshDashboard() {
            const data = dataset[currentIndex];
            document.getElementById('periodText').innerText = data.label;

            // تحديث المربعات العلوية
            const topGrid = document.getElementById('topGrid');
            topGrid.innerHTML = '';
            data.top.forEach((val, i) => {
                topGrid.innerHTML += `
                    <div class="top-card">
                        <div class="top-label">${topTitles[i]}</div>
                        <div class="top-val safe">${val}</div>
                    </div>`;
            });

            // تحديث الـ 5 أعمدة السفلية (بدون أسماء، فقط أرقام وأعمدة موسيقى)
            const censusGrid = document.getElementById('censusGrid');
            censusGrid.innerHTML = '';
            data.census.forEach((val, i) => {
                censusGrid.innerHTML += `
                    <div class="column-box">
                        <div class="column-val">${val}</div>
                        <div class="visualizer">
                            <div class="bar" style="animation-delay: ${Math.random()}s"></div>
                            <div class="bar" style="animation-delay: ${Math.random()}s"></div>
                            <div class="bar" style="animation-delay: ${Math.random()}s"></div>
                            <div class="bar" style="animation-delay: ${Math.random()}s"></div>
                        </div>
                        <div class="column-sub">Column ${i+1} Units</div>
                    </div>`;
            });

            // إضافة اسم الـ Staff في زاوية القسم السفلي بشكل احترافي
            censusGrid.innerHTML += `
                <div style="position:absolute; bottom:40px; right:40px; text-align:right">
                    <div style="font-size:0.6rem; color:#484f58">ON-DUTY STAFF</div>
                    <div style="font-size:0.9rem; font-weight:bold; color:var(--neon-blue)">${data.staff}</div>
                </div>`;

            currentIndex = (currentIndex + 1) % dataset.length;
        }

        refreshDashboard();
        setInterval(refreshDashboard, 20000); // التغير كل 20 ثانية
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=950, scrolling=False)
