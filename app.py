import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# إعدادات الصفحة (ثيم داكن وعريض)
st.set_page_config(page_title="AI ICU LIVE MONITOR", layout="wide")

# 1. تعريف البيانات والمؤشرات
kpi_configs = [
    {"title": "FALLS RATE", "max": 2.0},
    {"title": "HAPI INDEX", "max": 30.0},
    {"title": "CLABSI", "max": 5.0},
    {"title": "VAE EVENTS", "max": 7.0},
    {"title": "TURNOVER", "max": 10.0}
]

# سجل البيانات (كل صف يمثل ربع سنة - 3 شهور)
data_history = [
    [0.00, 26.67, 1.10, 1.05, 1.40],
    [0.24, 6.45, 2.67, 2.42, 4.34],
    [0.24, 14.29, 2.42, 0.00, 6.25],
    [0.36, 6.90, 2.63, 1.40, 4.69],
    [0.00, 9.68, 1.10, 1.40, 1.35]
]
quarters = ["4Q 2023", "1Q 2024", "2Q 2024", "3Q 2024", "4Q 2024"]

# --- CSS التنسيق المتقدم للـ AI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background-color: #0B0E14; }
    .ai-title {
        text-align: center; font-size: 48px; font-family: 'Orbitron';
        background: linear-gradient(90deg, #00f2ff, #7000ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
    }
    .ai-card {
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 20px; padding: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
    }
    .ai-circle {
        width: 100px; height: 100px; border-radius: 50%; margin: 0 auto 15px auto;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px; font-weight: bold; color: #00f2ff;
        border: 4px double #00f2ff; box-shadow: inset 0 0 10px #00f2ff;
    }
    .kpi-label { font-size: 10px; letter-spacing: 2px; color: #8892b0; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<p class="ai-title">ICU COMMAND CENTER</p>', unsafe_allow_html=True)
period_slot = st.empty()

st.write("---")

# إنشاء الحاويات للدوائر
cols = st.columns(len(kpi_configs))
kpi_slots = [c.empty() for c in cols]

st.write("---")
# حاوية الـ Bar Chart التلقائي
bar_chart_slot = st.empty()

# حلقة التحديث التلقائي (القلب النابض للداشبورد)
idx = 0
while True:
    current_vals = data_history[idx % len(data_history)]
    current_q = quarters[idx % len(quarters)]
    
    # 1. تحديث الفترة الزمنية
    period_slot.markdown(f"<h3 style='text-align: center; color: #8892b0; font-family: Orbitron;'>PERIOD: <span style='color: #00f2ff;'>{current_q}</span></h3>", unsafe_allow_html=True)
    
    # 2. تحديث الدوائر (الأرقام فقط تتغير)
    for i, slot in enumerate(kpi_slots):
        val = current_vals[i]
        title = kpi_configs[i]["title"]
        slot.markdown(f"""
            <div class="ai-card">
                <div class="kpi-label">{title}</div>
                <div class="ai-circle">{val}</div>
            </div>
        """, unsafe_allow_html=True)

    # 3. بناء وتحديث الـ Bar Chart التلقائي (Plotly)
    fig = go.Figure()
    
    # إضافة الأشرطة مع تأثير التدرج اللوني
    fig.add_trace(go.Bar(
        x=[k["title"] for k in kpi_configs],
        y=current_vals,
        marker=dict(
            color=current_vals,
            colorscale=[[0, '#00f2ff'], [1, '#7000ff']], # تدرج من اللبني للبنفسجي
            line=dict(color='#fff', width=1)
        ),
        text=current_vals,
        textposition='outside',
        textfont=dict(family="Orbitron", color="#fff")
    ))

    # إعدادات مظهر الشارت (Dark AI Theme)
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=450,
        yaxis=dict(title="Performance Value", gridcolor='rgba(255,255,255,0.1)', range=[0, 35]),
        xaxis=dict(font=dict(family="Orbitron", size=10)),
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        # أنيميشن داخلي بسيط عند التغير
        transition=dict(duration=800, easing="cubic-in-out")
    )

    # عرض الشارت في مكانه المخصص
    bar_chart_slot.plotly_chart(fig, use_container_width=True)
    
    # الانتظار 10 ثواني (دورة الربع السنوي)
    idx += 1
    time.sleep(10)
