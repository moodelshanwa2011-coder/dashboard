import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون بعرض كامل
st.set_page_config(layout="wide")

# كود الـ HTML والـ JS الخاص بك
html_code = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: sans-serif; background-color: #f0f4f8; margin: 0; padding: 10px; }
        .header { text-align: center; padding: 20px; background: #fff; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 30px; border-top: 5px solid #0056b3; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
        .card { background: #fff; border-radius: 15px; padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }
        .circle { width: 80px; height: 80px; border-radius: 50%; border: 6px solid #007bff; margin: 0 auto 10px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: bold; color: #007bff; }
        .label { font-weight: bold; color: #4a5568; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="header">
        <h2 style="color:#0056b3; margin:0;">لوحة مؤشرات ICU - الرياض</h2>
        <div style="margin-top:10px; font-weight:bold; color:#0056b3" id="qLabel">4Q 2023</div>
    </div>
    <div class="grid" id="kpiGrid"></div>
    <div style="background:white; margin-top:20px; padding:20px; border-radius:15px;"><canvas id="barChart" height="100"></canvas></div>

    <script>
        const data = [
            { q: "4Q 2023", v: [0, 7.3, 1.3, 1.5, 0, 5.2, 67, 13], b: [0.04, 26, 1.3, 1, 0.4, 1.6, 83, 8] },
            { q: "1Q 2024", v: [0.2, 6.4, 1.2, 2.1, 0.7, 4.8, 83, 20], b: [0.09, 7.7, 2.6, 2.4, 0.9, 4.4, 70, 19] },
            { q: "2Q 2024", v: [0, 6.5, 1.5, 2, 0.6, 3.7, 82, 18], b: [0.2, 14, 2.4, 1, 0.5, 6.2, 71, 12] }
        ];
        const labels = ["سقوط", "HAPI", "CLABSI", "VAE", "CAUTI", "Turnover", "BSN", "Hours"];
        let idx = 0; let chart;

        function update() {
            const cur = data[idx];
            document.getElementById('qLabel').innerText = cur.q;
            const grid = document.getElementById('kpiGrid');
            grid.innerHTML = '';
            cur.v.forEach((val, i) => {
                grid.innerHTML += `<div class="card"><div class="circle">${val}</div><div class="label">${labels[i]}</div></div>`;
            });
            if(!chart) {
                chart = new Chart(document.getElementById('barChart'), {
                    type: 'bar', data: { labels: labels, datasets: [{ data: cur.v, backgroundColor: '#007bff' }] }
                });
            } else { chart.data.datasets[0].data = cur.v; chart.update(); }
            idx = (idx + 1) % data.length;
        }
        update(); setInterval(update, 5000);
    </script>
</body>
</html>
"""

# عرض الكود داخل Streamlit
components.html(html_code, height=800, scrolling=True)
