import streamlit as st
import pandas as pd
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU AI Advanced Monitor", layout="wide")

# 2. البيانات المستخرجة من PDF (8 مؤشرات مختارة)
kpi_labels = [
    "FALLS RATE", "HAPI INDEX", "CLABSI", "VAE EVENTS", 
    "CAUTI", "RN BSN %", "TURNOVER", "NURSING HRS"
]

# البيانات مرتبة حسب الأرباع الزمنية الموجودة في الملف 
data_history = [
    # 4Q 2023, 1Q 2024, 2Q 2024, 3Q 2024, 4Q 2024
    [0.00, 26.67, 1.10, 1.05, 0.46, 83.53, 1.60, 19.09],
    [0.24, 6.45, 2.67, 2.42, 0.99, 70.31, 4.49, 12.54],
    [0.24, 14.29, 2.42, 0.00, 0.51, 71.21, 6.25, 19.20],
    [0.36, 6.90, 2.63, 1.40, 1.02, 82.74, 4.69, 12.39],
    [0.00, 9.68, 1.10, 1.40, 1.13, 83.36, 1.35, 19.82]
]
quarters = ["4Q 2023", "1Q 2024", "2Q 2024", "3Q 2024", "4Q 2024"]

# --- CSS التنسيق المستقبلي (Ultra-Modern) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background-color: #05070A; color: white; }
    
    .main-title {
        text-align: center; font-family: 'Orbitron'; font-size: 30px;
        background: linear-gradient(90deg, #00f2ff, #0072ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 5px; text-transform: uppercase; letter-spacing: 3px;
    }
    
    /* تصميم الكبسولة المضيئة (Modern Alternative to Circles) */
    .kpi-capsule {
        background: rgba(0, 242, 255, 0.02);
        border: 1px solid rgba(0, 242, 255, 0.15);
        border-radius: 50px; padding: 15px; text-align: center;
        transition: 0.5s; box-shadow: 0 0 10px rgba(0,0,0,0.5);
        margin-bottom: 15px;
    }
    .kpi-capsule:hover {
        border-color: #00f2ff; box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    }
    .val-text { font-family: 'Orbitron'; font-size: 22px; color: #00f2ff; font-weight: 700; }
    .label-text { font-size: 9px; color: #8B949E; letter-spacing: 1px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# الهيكل العلوي
st.markdown('<p class="main-title">ICU ADVANCED COMMAND CENTER</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#444; font-size:12px;'>SAUDI GERMAN HOSPITAL - RIYADH UNIT</p>", unsafe_allow_html=True)

# إدارة التحديث
if 'step' not in st.session_state: st.session_state.step = 0
idx = st.session_state.step % len(data_history)
vals = data_history[idx]

# عرض الربع الحالي بتنسيق نيون
st.markdown(f"<div style='text-align:center; margin-bottom:20px;'><span style='background:#00f2ff; color:#000; padding:2px 15px; border-radius:20px; font-family:Orbitron; font-size:12px;'>DATA STREAM: {quarters[idx]}</span></div>", unsafe_allow_html=True)

# 3. عرض الـ 8 مؤشرات (صفين في 4 أعمدة)
row1_cols = st.columns(4)
row2_cols = st.columns(4)
all_cols = row1_cols + row2_cols

for i in range(8):
    all_cols[i].markdown(f"""
        <div class="kpi-capsule">
            <div class="label-text">{kpi_labels[i]}</div>
            <div class="val-text">{vals[i]}</div>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# 4. البار تشارت "السمباتيك" والمستقر (بدون مكتبات خارجية لتجنب Error)
st.markdown("<p style='text-align:center; color:#555; font-family:Orbitron; font-size:10px;'>LIVE PERFORMANCE ANALYTICS</p>", unsafe_allow_html=True)

_, center_col, _ = st.columns([0.5, 2, 0.5])
with center_col:
    # استخدام الرسم البياني المدمج في Streamlit (مستقر 100%)
    chart_df = pd.DataFrame({'Score': vals}, index=kpi_labels)
    st.bar_chart(chart_df, color="#00f2ff", use_container_width=True)

# التحديث التلقائي
time.sleep(10)
st.session_state.step += 1
st.rerun()
