import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Performance Clean Monitor", layout="wide")

# 2. البيانات والـ Benchmarks (مستخرجة بدقة من ملف الرياض)
kpi_labels = ['FALLS RATE', 'HAPI INDEX', 'CLABSI', 'VAE EVENTS', 'CAUTI', 'RN BSN %', 'TURNOVER', 'NURSING HRS']
benchmarks = [0.14, 4.96, 1.26, 1.91, 0.43, 83.78, 3.97, 13.00] 

data_history = [
    [0.00, 26.67, 1.30, 1.06, 0.46, 83.53, 1.60, 19.09], # 4Q 2023
    [0.24, 6.45, 2.67, 2.42, 0.99, 70.31, 4.49, 12.54],  # 1Q 2024
    [0.24, 14.29, 2.42, 0.00, 0.51, 71.21, 6.25, 19.20], # 2Q 2024
    [0.36, 6.90, 2.63, 1.40, 1.02, 82.74, 4.69, 12.39],  # 3Q 2024
    [0.00, 9.68, 1.80, 1.60, 1.13, 83.36, 1.35, 19.82]   # 4Q 2024
]
quarters = ["4Q 2023", "1Q 2024", "2Q 2024", "3Q 2024", "4Q 2024"]

# --- CSS التنسيق النهائي (تركيز كامل على الكبسولات والدائرة) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background-color: #05070A; color: white; }
    .main-title { text-align: center; font-family: 'Orbitron'; font-size: 32px; color: #00f2ff; font-weight: bold; margin-bottom: 30px; }
    
    /* تصميم الكبسولات */
    .big-kpi-card { border-radius: 20px; padding: 30px 10px; text-align: center; margin-bottom: 20px; transition: 0.6s; }
    .normal { background: rgba(0, 242, 255, 0.03); border: 2px solid rgba(0, 242, 255, 0.2); }
    .critical { background: rgba(255, 0, 0, 0.15); border: 2px solid #ff0000; box-shadow: 0 0 25px rgba(255, 0, 0, 0.4); }
    
    .big-val { font-family: 'Orbitron'; font-size: 36px; font-weight: bold; }
    .color-normal { color: #00f2ff; text-shadow: 0 0 10px #00f2ff; }
    .color-critical { color: #ff0000; text-shadow: 0 0 15px #ff0000; }
    
    .big-label { font-size: 12px; color: #8B949E; letter-spacing: 2px; font-weight: bold; text-transform: uppercase; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">ICU PERFORMANCE INTELLIGENCE</p>', unsafe_allow_html=True)

# إدارة العداد للتحديث التلقائي
if 'step' not in st.session_state: st.session_state.step = 0
idx = st.session_state.step % len(data_history)
vals = data_history[idx]

st.markdown(f"<p style='text-align:center; font-family:Orbitron; color:#8B949E; margin-bottom:30px;'>STREAMING: <span style='color:#00f2ff;'>{quarters[idx]}</span></p>", unsafe_allow_html=True)

# 1. قسم الكبسولات (8 مؤشرات فقط)
row1 = st.columns(4)
row2 = st.columns(4)
all_cols = row1 + row2

for i in range(8):
    is_critical = False
    if kpi_labels[i] in ['RN BSN %', 'NURSING HRS']: 
        if vals[i] < benchmarks[i]: is_critical = True
    else: 
        if vals[i] > benchmarks[i]: is_critical = True
    
    card_class = "critical" if is_critical else "normal"
    text_class = "color-critical" if is_critical else "color-normal"
    
    all_cols[i].markdown(f"""
        <div class="big-kpi-card {card_class}">
            <div class="big-label">{kpi_labels[i]}</div>
            <div class="big-val {text_class}">{vals[i]}</div>
            <div style="font-size:9px; color:#555; margin-top:10px;">BENCHMARK: {benchmarks[i]}</div>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# 2. منطقة العرض المركزية (الدائرة فقط - بدون أي بارات)
_, center_col, _ = st.columns([1, 2, 1])

with center_col:
    # حساب نسبة الأمان
    safe_count = sum(1 for i in range(8) if not (
        (kpi_labels[i] in ['RN BSN %', 'NURSING HRS'] and vals[i] < benchmarks[i]) or 
        (kpi_labels[i] not in ['RN BSN %', 'NURSING HRS'] and vals[i] > benchmarks[i])
    ))
    safety_score = (safe_count / 8) * 100

    fig_donut = go.Figure(go.Pie(
        values=vals, labels=kpi_labels, hole=.82,
        marker=dict(colors=['#00f2ff', '#7000ff', '#0072ff', '#00d4ff', '#00b4ff', '#0094ff', '#0074ff', '#0054ff']),
        textinfo='none'
    ))
    fig_donut.update_layout(
        annotations=[dict(text=f'{int(safety_score)}%<br><span style="font-size:12px">SAFETY</span>', 
                     x=0.5, y=0.5, font_size=32, font_family="Orbitron", font_color="#00f2ff", showarrow=False)],
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500, showlegend=False, 
        margin=dict(t=0, b=0, l=0, r=0)
    )
    st.plotly_chart(fig_donut, use_container_width=True, key=f"donut_{st.session_state.step}")

# 3. التحديث التلقائي
time.sleep(10)
st.session_state.step += 1
st.rerun()
