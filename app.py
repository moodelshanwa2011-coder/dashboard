import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة (ثيم داكن)
st.set_page_config(page_title="ICU AI Dashboard", layout="wide")

# 2. البيانات المستخرجة من جدول المستشفى
kpi_labels = ["FALLS", "HAPI", "CLABSI", "VAE", "TURNOVER"]
data_history = [
    [0.00, 26.67, 1.10, 1.05, 1.40],
    [0.24, 6.45, 2.67, 2.42, 4.34],
    [0.24, 14.29, 2.42, 0.00, 6.25],
    [0.36, 6.90, 2.63, 1.40, 4.69],
    [0.00, 9.68, 1.10, 1.40, 1.35]
]
quarters = ["4Q 2023", "1Q 2024", "2Q 2024", "3Q 2024", "4Q 2024"]

# --- CSS لتنسيق واجهة الـ AI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');
    .stApp { background-color: #0B1015; }
    .ai-title { text-align: center; font-size: 35px; font-family: 'Orbitron'; color: #00f2ff; margin-bottom: 10px; }
    .ai-card { 
        background: rgba(0, 242, 255, 0.05); 
        border: 1px solid rgba(0, 242, 255, 0.3); 
        border-radius: 12px; padding: 15px; text-align: center;
    }
    .ai-circle { font-size: 24px; font-weight: bold; color: #fff; font-family: 'Orbitron'; margin: 5px 0; }
    .kpi-title { font-size: 11px; color: #8892b0; letter-spacing: 1px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<p class="ai-title">ICU AI COMMAND CENTER</p>', unsafe_allow_html=True)

# إدارة حالة العداد (Step Counter) لمنع تداخل الرسوم
if "step" not in st.session_state:
    st.session_state.step = 0

# تحديد البيانات الحالية بناءً على العداد
current_idx = st.session_state.step % len(data_history)
current_vals = data_history[current_idx]
current_q = quarters[current_idx]

# --- بناء المحتوى داخل حاوية نظيفة ---
# 1. عرض الفترة الزمنية
st.markdown(f"<p style='text-align: center; color: #8892b0; font-family: Orbitron;'>PERIOD: <span style='color: #00f2ff;'>{current_q}</span></p>", unsafe_allow_html=True)

# 2. عرض الدوائر (KPIs)
cols = st.columns(5)
for i, col in enumerate(cols):
    col.markdown(f"""
        <div class="ai-card">
            <div class="kpi-title">{kpi_labels[i]}</div>
            <div class="ai-circle">{current_vals[i]}</div>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# 3. عرض البار تشارت (مساحة أصغر + إظهار المحاور)
# استخدام أعمدة جانبية لتصغير عرض البار (0.7 مساحة فارغة يمين ويسار)
_, center_col, _ = st.columns([0.7, 2, 0.7])

with center_col:
    fig = go.Figure(go.Bar(
        x=kpi_labels,
        y=current_vals,
        marker=dict(color='#00f2ff', line=dict(color='#ffffff', width=0.5)),
        text=current_vals,
        textposition='outside',
        textfont=dict(color='#00f2ff', family='Orbitron')
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=380,
        margin=dict(l=50, r=20, t=50, b=50),
        xaxis=dict(
            tickfont=dict(color='#8892b0', family='Orbitron'),
            showgrid=False,
            linecolor='#8892b0'
        ),
        yaxis=dict(
            title="Performance Value",
            titlefont=dict(color='#8892b0', size=12),
            tickfont=dict(color='#8892b0'),
            gridcolor='rgba(255,255,255,0.05)',
            range=[0, 35]
        ),
        showlegend=False
    )
    
    # عرض الرسم البياني (بدون Key لمنع الـ ValueError مع rerun)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- منطق التحديث التلقائي ---
time.sleep(10)
st.session_state.step += 1
st.rerun()
