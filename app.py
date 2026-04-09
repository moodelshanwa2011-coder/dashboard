import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون بملء الشاشة وبدون هوامش
st.set_page_config(
    page_title="SGH Riyadh | ICU Executive Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# كود الواجهة الديناميكي (HTML/CSS/JS)
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #030712;
            --card-bg: rgba(15, 23, 42, 0.7);
            --neon-blue: #22d3ee;
            --neon-red: #f43f5e;
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
            --border-clr: rgba(255, 255, 255, 0.1);
        }
        
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
            overflow: hidden;
            display: flex;
            justify-content: center;
        }

        .dashboard-wrapper {
            width: 100%;
            max-width: 1600px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        /* رأس الصفحة عصري */
        .modern-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 40px;
            background: var(--card-bg);
            backdrop-filter: blur(15px);
            border-radius: 16px;
            border: 1px solid var(--border-clr);
        }

        .title-group h1 { margin: 0; font-size: 1.4rem; color: var(--neon-blue); }
        .title-group p { margin: 3px 0 0 0; color: var(--text-dim); font-size: 0.8rem; }
        
        .q-badge {
            background: linear-gradient(135deg, #0891b2, #22d3ee);
            color: #020617;
            padding: 8px 25px;
            border-radius: 10px;
            font-weight: 800;
            font-size: 1.2rem;
        }

        /* شبكة الحاويات الثمانية الضخمة */
        .mega-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            flex-grow: 1;
        }

        .mega-container {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid var(--border-clr);
            display: flex;
            flex-direction: column;
            align-items: center;
            transition: 0.3s ease;
        }

        .mega-container:hover {
            border-color: var(--neon-blue);
            transform: translateY(-5px);
        }

        .container-title {
            font-size: 0.9rem;
            font-weight: 800;
            color: var(--neon-blue);
            text-transform: uppercase;
            margin-bottom: 15px;
            letter-spacing: 1px;
            text-align: center;
        }

        /* تصميم الدوائر الاحترافية داخل الحاويات */
        .circles-row {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            width: 100%;
        }

        .circle-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            width: calc(50% - 5px);
        }

        .kpi-circle {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            border: 6px solid rgba(255, 255, 255, 0.05);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            transition: all 1s ease;
        }

        /* ألوان المؤشرات بناءً على الأداء (Safe=Cyan, Alert=Red) */
        .safe { border-color: var(--neon-blue); color: var(--neon-blue); text-shadow: 0 0 10px rgba(34, 211, 238, 0.4); }
        .alert { border-color: var(--neon-red); color: var(--neon-red); text-shadow: 0 0 10px rgba(244, 63, 94, 0.4); }

        .circle-val {
            font-size: 1.5rem;
            font-weight: 900;
        }

        .sub-title { font-size: 0.65rem; font-weight: 600; color: var(--text-dim); margin-top: 8px; max-width: 90%; }
        .bm-text { font-size: 0.6rem; color: #475569; font-style: italic; margin-top: 3px; }

        /* منطقة الـ Music Visualizer Chart */
        .chart-box {
            background: var(--card-bg);
            border-radius: 16px;
            padding: 15px 30px;
            border: 1px solid var(--border-clr);
            height: 250px;
        }
    </style>
</head>
<body>

<div class="dashboard-wrapper">
    <div class="modern-header">
        <div class="title-group">
            <h1>ICU PERFORMANCE | Executive Monitor</h1>
            <p>Saudi German Hospital - Riyadh | Clinical Operations Live Tracking</p>
        </div>
        <div class="q-badge" id="periodDisplay">4Q 2023</div>
    </div>

    <div class="mega-grid" id="dashboardGrid"></div>

    <div class="chart-box">
        <canvas id="musicChart"></canvas>
    </div>
</div>

<script>
    // البيانات الفعلية المستخرجة من جدول PDF (Falls, Injuries, CLABSI, VAE, CAUTI, Education, Turnover, Restraints)
    const timelineData = [
        { q: "4Q 2023", v: [0, 7.3, 1.38, 1.57, 0, 67, 5.21, 23.3], b: [0.04, 26.6, 1.3, 1.06, 0.46, 83.5, 1.6, 5.08] },
        { q: "1Q 2024", v: [0.24, 6.45, 1.28, 2.17, 0.70, 83, 4.84, 6.45], b: [0.09, 7.7, 2.67, 2.42, 0.99, 70.3, 4.49, 6.47] },
        { q: "2Q 2024", v: [0.06, 6.54, 1.56, 2.04, 0.67, 82.7, 3.74, 6.84], b: [0.24, 14.2, 2.42, 2.04, 0.67, 71.2, 6.25, 6.84] },
        { q: "3Q 2024", v: [0.28, 4.60, 1.20, 1.89, 0.40, 83.3, 4.51, 6.32], b: [0.36, 6.9, 2.63, 0, 1.02, 68.2, 4.69, 6.32] },
        { q: "1Q 2025", v: [1.59, 4.17, 1.26, 1.91, 0.43, 83.7, 1.43, 8.23], b: [0.12, 4.9, 3.02, 6.69, 0, 70, 3.97, 8.23] }
    ];

    // أسماء الأقسام والدوائر الفرعية بناءً على الـ PDF
    const sections = [
        { title: "Falls Metric", subs: ["Total Patient Falls", "Injury Falls"] },
        { title: "Pressure Injury", subs: ["HAPI % Surveyed", "HAPI Stage II+"] },
        { title: "Infections", subs: ["CLABSI per 1k days", "VAE per 1k days"] },
        { title: "Device infections", subs: ["CAUTI per 1k days", "Total C-diff"] },
        { title: "Respiratory", subs: ["VAE Event Rate", "VAP Rate"] },
        { title: "Education & Retention", subs: ["RN BSN %", "Staff Turnover %"] },
        { title: "Restraints & MDRO", subs: ["Physical Restraints %", "Total MDRO-MRSA"] },
        { title: "Staffing & Assault", subs: ["Total RN Hrs/Patient Day", "Staff Assault Rate"] }
    ];

    let currentIndex = 0;
    let visualizerChart;

    function renderUI() {
        const d = timelineData[currentIndex];
        document.getElementById('periodDisplay').innerText = d.q;
        const grid = document.getElementById('dashboardGrid');
        grid.innerHTML = '';

        sections.forEach((s, i) => {
            // كل قسم (حاوية) تحتوي على دائرتين فرعيتين (subs)
            let subsHtml = '';
            for(let j=0; j<2; j++) {
                const valIdx = i * 2 + j;
                const val = d.v[valIdx];
                const bm = d.b[valIdx];
                // منطق الحساب: بعض المؤشرات (BSN, Hours) الأفضل هو الزيادة، والبعض الآخر الأفضل هو النقصان
                const higherIsBetter = (valIdx === 10 || valIdx === 14);
                const isBad = higherIsBetter ? (val < bm) : (val > bm);
                const statusCls = isBad ? 'alert' : 'safe';

                subsHtml += `
                    <div class="circle-box">
                        <div class="kpi-circle ${statusCls}">
                            <div class="circle-val">${val}</div>
                        </div>
                        <div class="sub-title">${s.subs[j]}</div>
                        <div class="bm-text">BM: ${bm}</div>
                    </div>`;
            }

            grid.innerHTML += `
                <div class="mega-container">
                    <div class="container-title">${s.title}</div>
                    <div class="circles-row">${subsHtml}</div>
                </div>`;
        });

        // تحديث الـ Visualizer Chart
        const summaryData = sections.map((s, i) => (d.v[i*2] + d.v[i*2+1]) / 2); // متوسط بيانات القسم
        if(!visualizerChart) {
            const ctx = document.getElementById('musicChart').getContext('2d');
            visualizerChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: sections.map(s => s.title),
                    datasets: [{
                        data: summaryData,
                        backgroundColor: '#22d3ee',
                        borderRadius: 10,
                        barThickness: 35
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    animation: { duration: 1000, easing: 'easeInOutQuart' }, // حركة ناعمة لشبه الأعمدة الموسيقية
                    scales: {
                        y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.03)' }, ticks: { color: '#64748b', font: { size: 10 } } },
                        x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 11, weight: 'bold' } } }
                    }
                }
            });
        } else {
            visualizerChart.data.datasets[0].data = summaryData;
            visualizerChart.update();
        }

        currentIndex = (currentIndex + 1) % timelineData.length;
    }

    renderUI();
    setInterval(renderUI, 20000); // تحديث كل 20 ثانية كما طلبت
</script>
</body>
</html>
"""

# عرض اللوحة في Streamlit بدون شريط جانبي
components.html(dashboard_html, height=1000, scrolling=False)
