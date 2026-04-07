import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU AI Dashboard", layout="wide")

# 2. البيانات
kpi_labels = ["FALLS", "HAPI", "CLABSI", "VAE", "TURNOVER"]
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
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');
    .stApp { background-color: #0B0E14; }
    .ai-title { text-align: center; font-size: 35px; font-family: 'Orbitron'; color: #00f2ff; margin-bottom: 20px; }
    .ai-card { 
        background: rgba(0, 242, 255, 0.03); 
        border: 1px solid rgba(0, 242, 255, 0.3); 
        border-radius: 15px; padding: 15px; text-align: center;
    }
    .ai-circle { font-size: 22px; font-weight: bold; color: #fff; margin: 10px 0; font-family: 'Orbitron'; }
    .kpi-title { font-size: 11px; color: #8892b0; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="ai-title">ICU COMMAND CENTER</p>', unsafe_allow_html=True)
period_slot = st.empty()

st.write("---")

# منطقة الدوائر
cols = st.columns(5)
kpi_slots = [c.empty() for c in cols]

st.write("---")

# --- تصغير مساحة البار (وضعه في عمود أوسط) ---
left_spacer, center_cont, right_spacer = st.columns([0.5, 2, 0.5]) # تعديل النسب لتوسيع البار قليلاً مع بقائه سمباتيك
with center_cont:
    bar_chart_slot = st.empty()

# --- حلقة التحديث الذكية ---
idx = 0
while True:
    current_vals = data_history[idx % len(data_history)]
    current_q = quarters[idx % len(quarters)]
    
    # تحديث النص العلوي
    period_slot.markdown(f"<p style='text-align: center; color: #8892b0; font-family: Orbitron;'>SYSTEM STATUS: <span style='color: #00f2ff;'>ACTIVE</span> | STREAM: {current_q}</p>", unsafe_allow_html=True)
    
    # تحديث الدوائر
    for i, slot in enumerate(kpi_slots):
        slot.markdown(f"""
            <div class="ai-card">
                <div class="kpi-title">{kpi_labels[i]}</div>
                <div class="ai-circle">{current_vals[i]}</div>
            </div>
        """, unsafe_allow_html=True)

    # بناء الرسم البياني مع إظهار المحاور (Axis)
    fig = go.Figure(go.Bar(
        x=kpi_labels,
        y=current_vals,
        marker=dict(
            color='#00f2ff',
            line=dict(color='#fff', width=0.5)
        ),
        text=current_vals,
        textposition='outside',
        textfont=dict(color='#00f2ff', family='Orbitron')
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        font=dict(color='#8892b0', family='Orbitron'),
        margin=dict(l=40, r=20, t=40, b=40),
        # إعدادات المحاور لإظهارها بوضوح
        yaxis=dict(
            title="Performance Value",
            visible=True, 
            showgrid=True, 
            gridcolor='rgba(255,255,255,0.05)', # شبكة خفيفة جداً
            zeroline=True,
            zerolinecolor='rgba(0,242,255,0.2)',
            range=[0, 35]
        ),
        xaxis=dict(
            showgrid=False,
            linecolor='rgba(0,242,255,0.2)', # خط المحور السفلي
            linewidth=2
        ),
        showlegend=False
    )

    # استخدام key متغير يمنع تعارض العناصر في الذاكرة
    bar_chart_slot.plotly_chart(fig, use_container_width=True, key=f"v_{idx}")
    
    idx += 1
    time.sleep(10)
