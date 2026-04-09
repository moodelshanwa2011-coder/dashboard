import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="SGH Riyadh | ICU Performance Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تحضير البيانات المستخرجة من الـ PDF
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
            margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .q-badge {
            background: linear-gradient(135deg, #0891b2, #22d3ee);
            color: #020617; padding: 8px 25px; border-radius: 10px;
            font-weight: 900; font-size: 1.2rem;
        }

        /* شبكة المؤشرات العلوية */
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px; }

        .kpi-card {
            background: var(--card-bg); border-radius: 18px; padding: 20px;
            text-align: center; border: 2px solid var(--border-clr);
            transition: 0.4s;
        }

        .val-large { font-size: 2.8rem; font-weight: 900; line-height: 1; margin: 10px 0; }
        .safe { color: var(--neon-blue); text-shadow: 0 0 10px rgba(34, 211, 238, 0.3); }
        .alert { color: var(--neon-red); text-shadow: 0 0 10px rgba(244, 63, 94, 0.3); }

        .bm-label { font-size: 0.75rem; color: #64748b; background: rgba(255,255,255,0.05); padding: 4px 10px; border-radius: 5px; }

        /* القسم السفلي للأرقام المتغيرة داخل الدوائر */
        .bottom-section { display: grid; grid-template-columns: 1.8fr 1.2fr; gap: 20px; height: 350px; }

        .panel {
            background: var(--card-bg); border-radius: 20px; padding: 20px;
            border: 1px solid var(--border-clr);
        }

        .circles-container { display: flex; justify-content: space-around; align-items: center; height: 100%; }

        .score-box { text-align: center; }

        .circle {
            width: 150px; height: 150px; border-radius: 50%;
            border: 8px solid #1e293b; display: flex; flex-direction: column;
            align-items: center; justify-content: center; transition: 1s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .circle-val { font-size: 2.2rem; font-weight: 900; }
        .circle-txt { font-size: 0.7rem; font-weight: bold; color: #94a3b8; margin-top: 5px; text-transform: uppercase; }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1 style="margin:0; font-size:1.4rem;">SAUDI GERMAN HOSPITAL | <span style="color:var(--neon-blue)">ICU RIYADH</span></h1>
            <p style="margin:2px 0 0 0; color:#64748b; font-size:0.8rem;">Clinical Quality Performance Tracking </p>
        </div>
        <div class="q-badge" id="qLabel">4Q 2023</div>
    </div>

    <div class="grid" id="kpiGrid"></div>

    <div class="bottom-section">
        <div class="panel">
            <canvas id="liveChart"></canvas>
        </div>

        <div class="panel">
            <div class="circles-container">
                <div class="score-box">
                    <div class="circle" id="circle1">
                        <div class="circle-val" id="val1">0%</div>
                    </div>
                    <div class="circle-txt">HAPI % </div>
                </div>
                <div class="score-box">
                    <div class="circle" id="circle2">
                        <div class="circle-val" id="val2">0%</div>
                    </div>
                    <div class="circle-txt">RN BSN % </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // البيانات الفعلية المستخرجة من جدول PDF 
        const dataLog = [
            { q: "4Q 2023", v: [0, 7.30, 1.38, 1.57, 0, 5.21, 67.19, 13.0], b: [0.04, 26.67, 1.3, 1.06, 0.46, 1.6, 83.53, 8.0] },
            { q: "1Q 2024", v: [0.24, 6.45, 1.28, 2.17, 0.70, 4.84, 82.99, 20.1], b: [0.09, 7.77, 2.67, 2.42, 0.99, 4.49, 70.31, 19.1] },
            { q: "2Q 2024", v: [0.06, 6.54, 1.56, 2.04, 0.67, 3.74, 82.74, 18.22], b: [0.24, 14.29, 2.42, 2.04, 0.67, 6.25, 71.21, 12.54] },
            { q: "3Q 2024", v: [0.28, 4.60, 1.20, 1.89, 0.40, 4.51, 83.36, 18.34], b: [0.36, 6.9, 2.63, 0, 1.02, 4.69, 68.25, 12.39] },
            { q: "1Q 2025", v: [1.59, 4.17, 1.26, 1.91, 0.43, 1.43, 83.78, 18.28], b: [0.12, 4.96, 3.02, 6.69, 0, 3.97, 70, 12.71] }
        ];

        const labels = ["Falls", "HAPI", "CLABSI", "VAE", "CAUTI", "Turnover", "BSN %", "RN Hours"];
        let step = 0;
        let chart;

        function update() {
            const current = dataLog[step];
            document.getElementById('qLabel').innerText = current.q;

            // تحديث الكروت العلوية
            const grid = document.getElementById('kpiGrid');
            grid.innerHTML = '';
            current.v.forEach((val, i) => {
                const isBad = (i < 6) ? (val > current.b[i]) : (val < current.b[i]);
                grid.innerHTML += `
                    <div class="kpi-card">
                        <div style="font-size:0.75rem; color:#94a3b8; font-weight:700;">${labels[i]}</div>
                        <div class="val-large ${isBad?'alert':'safe'}">${val}</div>
                        <div class="bm-label">Benchmark: ${current.b[i]}</div>
                    </div>`;
            });

            // تحديث الأرقام داخل الدوائر (HAPI و BSN Education)
            const hapiVal = current.v[1];
            const bsnVal = Math.round(current.v[6]);
            
            document.getElementById('val1').innerText = hapiVal + "%";
            document.getElementById('val2').innerText = bsnVal + "%";
            
            // تغيير ألوان الدوائر بناءً على الأداء
            document.getElementById('circle1').style.borderColor = hapiVal > current.b[1] ? "#f43f5e" : "#22d3ee";
            document.getElementById('circle2').style.borderColor = bsnVal < current.b[6] ? "#f43f5e" : "#22d3ee";

            // تحديث الرسم البياني
            if (!chart) {
                const ctx = document.getElementById('liveChart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'bar',
                    data: { labels: labels, datasets: [{ data: current.v, backgroundColor: '#22d3ee', borderRadius: 5 }] },
                    options: { maintainAspectRatio: false, plugins: { legend: { display: false } },
                               scales: { y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } } } }
                });
            } else {
                chart.data.datasets[0].data = current.v;
                chart.update();
            }

            step = (step + 1) % dataLog.length;
        }

        update();
        setInterval(update, 20000); // تحديث كل 20 ثانية كما طلبت
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=900, scrolling=False)
