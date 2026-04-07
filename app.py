import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU AI Radar Monitor", layout="wide")

# 2. البيانات (8 مؤشرات من ملف الرياض)
categories = ['FALLS', 'HAPI', 'CLABSI', 'VAE', 'CAUTI', 'RN BSN%', 'TURNOVER', 'NURSING HRS']
data_history = [
    [0.00, 26.67, 1.10, 1.05, 0.46, 83.53, 1.60, 19.09],
    [0.24, 6.45, 2.67, 2.42, 0.99, 70.31, 4.49, 12.54],
    [0.24, 14.29, 2.42, 0.00, 0.51, 71.21, 6.25, 19.20],
    [0.36, 6.90, 2.63, 1.40, 1.02, 82.74, 4.69, 12.39],
    [0.00, 9.68, 1.10, 1.40, 1.13, 83.36, 1.35, 19.82]
]
quarters = ["4Q 2023", "1Q 2024", "2Q 2024", "3Q 2024", "4Q 2024"]

# --- CSS التنسيق المستقبلي ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background-color: #05070A; color: white; }
    .main-title {
        text-align: center; font-family: 'Orbitron'; font-size: 32px;
        background: linear-gradient(90deg, #00f2ff, #7000ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: 2px; font-weight: bold; margin-bottom: 20px;
    }
    .modern-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(0, 242, 255, 0.1);
        border-radius: 15px; padding: 15px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
    }
    .val-neon { font-family: 'Orbitron'; font-size: 20px; color: #00f2ff; text-shadow: 0 0 10px #00f2ff; }
    .label-sub { font-size: 9px; color: #8B949E; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">ICU PERFORMANCE RADAR</p>', unsafe_allow_html=True)

# إدارة العداد
if 'step' not in st.session_state: st.session_state.step = 0
idx = st.session_state.step % len(data_history)
r_values = data_history[idx]

st.markdown(f"<p style='text-align:center; font-family:Orbitron; color:#8B949E;'>LIVE STREAM: <span style='color:#7000ff;'>{quarters[idx]}</span></p>", unsafe_allow_html=True)

# 3. عرض المؤشرات (8 كبسولات نيون)
cols = st.columns(8)
for i in range(8):
    cols[i].markdown(f"""
        <div class="modern-card">
            <div class="label-sub">{categories[i]}</div>
            <div class="val-neon">{r_values[i]}</div>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# 4. الرادار تشارت (أحدث وأقوى شكل بياني للذكاء الاصطناعي)
_, center_col, _ = st.columns([0.5, 2, 0.5])
with center_col:
    # بناء الرادار
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r_values + [r_values[0]], # لغلق الدائرة
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(0, 242, 255, 0.2)',
        line=dict(color='#00f2ff', width=2),
        marker=dict(color='#7000ff', size=8),
        name=quarters[idx]
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.05)", showticklabels=False),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(family="Orbitron", size=10, color="#8B949E"))
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=500,
        margin=dict(l=80, r=80, t=20, b=20),
        showlegend=False
    )

    # عرض الرادار مع Key ديناميكي لمنع الـ Error
    st.plotly_chart(fig, use_container_width=True, key=f"radar_{st.session_state.step}")

# التحديث التلقائي
time.sleep(10)
st.session_state.step += 1
st.rerun()
