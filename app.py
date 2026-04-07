import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة الاحترافية
st.set_page_config(
    page_title="ICU Riyadh | Modern Executive Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# كود الواجهة المحدث (Modern Squares + Professional Colors)
dashboard_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #030712;
            --card-bg: rgba(30, 41, 59, 0.5);
            --accent: #38bdf8;
            --danger: #f43f5e;
            --border: rgba(255, 255, 255, 0.1);
            --text-p: #94a3b8;
        }
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--bg);
            color: #f8fafc;
            margin: 0;
            padding: 25px;
            overflow: hidden;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--card-bg);
            backdrop-filter: blur(15px);
            padding: 20px 40px;
            border-radius: 20px;
            border: 1px solid var(--border);
            margin-bottom: 25px;
        }
        .q-badge {
            background: linear-gradient(135deg, #0ea5e9, #38bdf8);
            color: #030712;
            padding: 8px 25px;
            border-radius: 10px;
            font-weight: 800;
            font-size: 1.2rem;
            box-shadow: 0 10px 20px rgba(56, 189, 248, 0.2);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 25px;
        }
        /* تصميم المربعات Modern Squares */
        .square-card {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 25px;
            text-align: center;
            transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .square-card:hover {
            transform: translateY(-5px);
            border-color: var(--accent);
            background: rgba(56, 189, 248, 0.05);
        }
        .value-box {
            font-size: 2.2rem;
            font-weight: 900;
            margin-bottom: 10px;
            letter-spacing: -1px;
        }
        .safe { color: var(--accent); text-shadow: 0 0 20px rgba(56, 189, 248, 0.3); }
        .alert { color: var(--danger); text-shadow: 0 0 20px rgba(244, 63, 94, 0.3); }
        
        .label { font-size: 0.95rem; font-weight: 600; color: var(--text-p); }
        .bm-ref { font-size: 0.75rem; color: #475569; margin-top: 8px; }

        .chart-box {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            height: 320px;
            border: 1px solid var(--border);
        }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1 style="margin:0; font-size:1.6rem; letter-spacing:1px;">ICU PERFORMANCE <span style="color:var(--accent)">ANALYSIS</span></h1>
            <p style="margin:5px 0 0 0; color:var(--text-p); font-size:0.85rem;">Saudi German Hospital | Riyadh</p>
        </div>
        <div class="q-badge" id="qLabel">4Q 2023</div>
    </div>

    <div class="grid" id="kpiGrid"></div>

    <div class="chart-box">
        <canvas id="mainChart"></canvas>
    </div>

    <script>
        const timeline = [
            { q: "4Q 2023", v: [0, 7.3, 1.3, 1.5, 0, 5.2, 67, 13], b: [0.04, 26, 1.3, 1, 0.4, 1.6, 83, 8] },
            { q: "1Q 2024", v: [0.2, 6.4, 1.2, 2.1, 0.7, 4.8, 83, 20], b: [0.09, 7.7, 2.6, 2.4, 0.9, 4.4, 70, 19] },
            { q: "2Q 2024", v: [0.0, 6.5, 1.5, 2.0, 0.6, 3.7, 82, 18], b: [0.2, 14, 2.4, 1, 0.5, 6.2, 71, 12] },
            { q: "3Q 2024", v: [0.2, 4.6, 1.2, 1.8, 0.4, 4.5, 83, 18], b: [0.3, 6.9, 2.6, 1, 1, 4.6, 68, 19] }
        ];
        const titles = ["سقوط المرضى", "إصابات الضغط", "عدوى الدم", "VAE تنفس", "CAUTI مسالك", "دوران العمل", "تعليم BSN", "ساعات RN"];
        let idx = 0; let chart;

        function update() {
            const data = timeline[idx];
            document.getElementById('qLabel').innerText = data.q;
            const grid = document.getElementById('kpiGrid');
            grid.innerHTML = '';

            data.v.forEach((v, i) => {
                const isBad = (i < 6) ? (v > data.b[i]) : (v < data.b[i]);
                const cls = isBad ? 'alert' : 'safe';
                grid.innerHTML += `
                    <div class="square-card">
                        <div class="value-box ${cls}">${v}</div>
                        <div class="label">${titles[i]}</div>
                        <div class="bm-ref">Benchmark: ${data.b[i]}</div>
                    </div>`;
            });

            if(!chart) {
                const ctx = document.getElementById('mainChart').getContext('2d');
                chart = new Chart(ctx, {
                    type: 'bar',
                    data: { 
                        labels: titles, 
                        datasets: [{ 
                            data: data.v, 
                            backgroundColor: '#38bdf8', 
                            borderRadius: 6,
                            barThickness: 25 // تقليل عرض البار ليكون أرفع وأجمل
                        }] 
                    },
                    options: { 
                        maintainAspectRatio: false, 
                        plugins: { legend: { display: false } },
                        scales: { 
                            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } },
                            x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 11 } } }
                        }
                    }
                });
            } else {
                chart.data.datasets[0].data = data.v;
                chart.data.datasets[0].backgroundColor = data.v.map((v, i) => 
                    (i < 6 ? v > data.b[i] : v < data.b[i]) ? '#f43f5e' : '#38bdf8'
                );
                chart.update();
            }
            idx = (idx + 1) % timeline.length;
        }
        update(); setInterval(update, 8000);
    </script>
</body>
</html>
"""

# عرض الداش بورد
components.html(dashboard_html, height=900, scrolling=False)
