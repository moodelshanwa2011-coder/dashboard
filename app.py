import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU AI Monitor", layout="wide")

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

# --- CSS لتنسيق الـ AI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');
    .stApp { background-color: #0B1015; color: white; }
    .ai-card { 
        background: #161B22; border: 1px solid #00f2ff; border-radius: 12px; 
        padding: 15px; text-align: center; 
    }
    .kpi-val { font-family: 'Orbitron'; font-size: 24px; color: #00f2ff; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#00f2ff; font-family:Orbitron;'>ICU COMMAND CENTER</h1>", unsafe_allow_html=True)

# إدارة العداد
if 'step' not in st.session_state:
    st.session_state.step = 0

idx = st.session_state.step % len(data_history)
vals = data_history[idx]
q_label = quarters[idx]

st.markdown(f"<p style='text-align:center; color:#8B949E;'>PERIOD: {q_label}</p>", unsafe_allow_html=True)

# 3. عرض الكروت (الدوائر المطورة)
cols = st.columns(5)
for i in range(5):
    cols[i].markdown(f"""
        <div class="ai-card">
            <div style="font-size:10px; color:#8B949E;">{kpi_labels[i]}</div>
            <div class="kpi-val">{vals[i]}</div>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# 4. البار تشارت (Matplotlib) - حل مشكلة الـ Error نهائياً
left, center, right = st.columns([0.8, 2, 0.8])
with center:
    fig, ax = plt.subplots(figsize=(6, 3))
    # لون الخلفية ليطابق الـ Dark Mode
    fig.patch.set_facecolor('#0B1015')
    ax.set_facecolor('#0B1015')
    
    bars = ax.bar(kpi_labels, vals, color='#00f2ff', edgecolor='white', linewidth=0.5)
    
    # إظهار المحاور (Axis)
    ax.set_ylabel('Performance Value', color='#8B949E', fontsize=8)
    ax.tick_params(axis='x', colors='#8B949E', labelsize=7)
    ax.tick_params(axis='y', colors='#8B949E', labelsize=7)
    ax.spines['bottom'].set_color('#8B949E')
    ax.spines['left'].set_color('#8B949E')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # إضافة الأرقام فوق الأعمدة
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5, f'{height}', ha='center', va='bottom', color='#00f2ff', fontsize=7)

    st.pyplot(fig)

# 5. التحديث التلقائي المستقر
time.sleep(10)
st.session_state.step += 1
st.rerun()
