import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# إعدادات الصفحة
st.set_page_config(page_title="AI ICU LIVE MONITOR", layout="wide")

# 1. البيانات
kpi_configs = [
    {"title": "FALLS RATE", "max": 2.0},
    {"title": "HAPI INDEX", "max": 30.0},
    {"title": "CLABSI", "max": 5.0},
    {"title": "VAE EVENTS", "max": 7.0},
    {"title": "TURNOVER", "max": 10.0}
]

data_history = [
    [0.00, 26.67, 1.10, 1.05, 1.40],
    [0.24, 6.45, 2.67, 2.42, 4.34],
    [0.24, 14.29, 2.42, 0.00, 6.25],
    [0.36, 6.90, 2.63, 1.40, 4.69],
    [0.00, 9.68, 1.10, 1.40, 1.35]
]
quarters = ["4Q 2023", "1Q 2024", "2Q 2024", "3Q 2024", "4Q 2024"]

# --- CSS التنسيق المتقدم ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background-color: #0B0E14; }
    .ai-title {
        text-align: center; font-size: 40px; font-family: 'Orbitron';
        background: linear-gradient(90deg, #00f2ff, #7000ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .ai-card {
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 15px; padding: 15px; text-align: center;
    }
    .ai-circle {
        width: 90px; height: 90px; border-radius: 50%; margin: 0 auto 10px auto;
        display: flex; align-items: center; justify-content: center;
        font-size: 20px; font-weight: bold; color: #00f2ff;
        border: 3px double #00f2ff; box-shadow: inset 0 0 10px #00f2ff;
    }
    .kpi-label { font-size: 10px; color: #8892b0; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="ai-title">ICU COMMAND CENTER</p>', unsafe_allow_html=True)
period_slot = st.empty()

st.write("---")
cols = st.columns(len(kpi_configs))
kpi_slots = [c.empty() for c in cols]

st.write("---")
bar_chart_slot = st.empty()

idx = 0
while True:
    current_vals = data_history[idx % len(data_history)]
    current_q = quarters[idx % len(quarters)]
    
    period_slot.markdown(f"<h3 style='text-align: center; color: #8892b0; font-family: Orbitron;'>PERIOD: <span style='color: #00f2ff;'>{current_q}</span></h3>", unsafe_allow_html=True)
    
    for i, slot in enumerate(kpi_slots):
        val = current_vals[i]
        title = kpi_configs[i]["title"]
        slot.markdown(f'<div class="ai-card"><div class="kpi-label">{title}</div><div class="ai-circle">{val}</div></div>', unsafe_allow_html=True)

    # بناء الرسم البياني بطريقة أكثر استقراراً
    fig = go.Figure(data=[
        go.Bar(
            x=[k["title"] for k in kpi_configs],
            y=current_vals,
            marker_color='#00f2ff',
            text=current_vals,
            textposition='outside'
        )
    ])

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(range=[0, 35]) # تحديد المدى الثابت يمنع القفز المزعج للأعمدة
    )

    bar_chart_slot.plotly_chart(fig, use_container_width=True, key=f"chart_{idx}")
    
    idx += 1
    time.sleep(10)
