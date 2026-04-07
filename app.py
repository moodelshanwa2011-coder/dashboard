import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_config = st.set_page_config(page_title="AI ICU Dashboard", layout="wide")

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

# --- CSS للجماليات ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');
    .stApp { background-color: #0B0E14; }
    .ai-title { text-align: center; font-size: 35px; font-family: 'Orbitron'; color: #00f2ff; margin-bottom: 10px; }
    .ai-card { background: rgba(0, 242, 255, 0.05); border: 1px solid #00f2ff; border-radius: 15px; padding: 10px; text-align: center; }
    .ai-circle { font-size: 20px; font-weight: bold; color: #fff; margin: 10px 0; font-family: 'Orbitron'; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="ai-title">ICU COMMAND CENTER</p>', unsafe_allow_html=True)
period_slot = st.empty()

# منطقة الدوائر
cols = st.columns(5)
kpi_slots = [c.empty() for c in cols]

st.write("---")

# --- حل مشكلة العرض (صغير في النص) ---
# نستخدم 3 أعمدة ونضع البار في المنتصف ليكون عرضه صغيراً واحترافياً
left_spacer, center_cont, right_spacer = st.columns([1, 2, 1])
with center_cont:
    bar_chart_slot = st.empty()

# --- حلقة التحديث ---
idx = 0
while True:
    current_vals = data_history[idx % len(data_history)]
    current_q = quarters[idx % len(quarters)]
    
    # تحديث الفترة
    period_slot.markdown(f"<p style='text-align: center; color: #8892b0;'>DATA STREAM: {current_q}</p>", unsafe_allow_html=True)
    
    # تحديث الدوائر
    for i, slot in enumerate(kpi_slots):
        slot.markdown(f"""
            <div class="ai-card">
                <div style="font-size: 10px; color: #00f2ff;">{kpi_labels[i]}</div>
                <div class="ai-circle">{current_vals[i]}</div>
            </div>
        """, unsafe_allow_html=True)

    # بناء البار تشارت (تصميم AI روعة)
    fig = go.Figure(go.Bar(
        x=kpi_labels,
        y=current_vals,
        marker=dict(color='#00f2ff', line=dict(color='#fff', width=1)),
        text=current_vals,
        textposition='outside'
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(visible=False, range=[0, 35]), # إخفاء المحور الجانبي لمظهر أنظف
        xaxis=dict(tickfont=dict(size=10, family='Orbitron'))
    )

    # عرض الشارت (استخدام حاوية empty يمنع الـ Error)
    bar_chart_slot.plotly_chart(fig, use_container_width=True, key=f"v_{idx}")
    
    idx += 1
    time.sleep(10)
