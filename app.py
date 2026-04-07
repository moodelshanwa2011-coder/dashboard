import streamlit as st
import pandas as pd
import time

# إعدادات الصفحة لتكون عريضة واحترافية
st.set_page_config(page_title="ICU KPI Dashboard", layout="wide")

# 1. تعريف عناوين الـ KPIs والقيم القصوى لكل منها (لضبط شريط التقدم)
kpi_configs = [
    {"title": "Patient Falls Rate", "max": 2.0},
    {"title": "HAPI (Pressure Injuries)", "max": 30.0},
    {"title": "CLABSI (Infections)", "max": 5.0},
    {"title": "VAE (Ventilator Events)", "max": 7.0},
    {"title": "Nurse Turnover %", "max": 10.0}
]

# 2. البيانات المستخرجة من جدول الصورة (دوران ربع سنوي)
quarterly_data = {
    "4Q 2023": [0.00, 26.67, 1.10, 1.05, 1.40],
    "1Q 2024": [0.24, 6.45, 2.67, 2.42, 4.34],
    "2Q 2024": [0.24, 14.29, 2.42, 0.00, 6.25],
    "3Q 2024": [0.36, 6.90, 2.63, 1.40, 4.69],
    "4Q 2024": [0.00, 9.68, 1.10, 1.40, 1.35]
}

quarters = list(quarterly_data.keys())

# إدارة التحديث التلقائي كل 10 ثواني
if 'index' not in st.session_state:
    st.session_state.index = 0

current_q = quarters[st.session_state.index % len(quarters)]
values = quarterly_data[current_q]

# --- العنوان الكبير في منتصف الصفحة ---
st.markdown(f"""
    <div style="text-align: center; margin-top: -50px; margin-bottom: 50px;">
        <h1 style="font-size: 50px; color: #2c3e50; font-family: 'Arial';">
            ICU DYNAMIC PERFORMANCE DASHBOARD
        </h1>
        <h2 style="color: #3498db; font-weight: normal;">
            Monitoring Period: {current_q}
        </h2>
    </div>
""", unsafe_allow_html=True)

st.write("---")

# إنشاء 5 أعمدة لكل KPI
cols = st.columns(len(kpi_configs))

for i, col in enumerate(cols):
    val = values[i]
    max_val = kpi_configs[i]["max"]
    title = kpi_configs[i]["title"]
    
    # حساب النسبة المئوية لشريط التقدم
    progress_val = min((val / max_val), 1.0) 
    
    # تحديد اللون: أخضر للأداء الجيد، أحمر للتنبيه
    color = "#2ecc71" if val < (max_val * 0.4) else "#e74c3c"
    
    with col:
        # 1. العنوان فوق الدائرة (مركز في المنتصف)
        st.markdown(f"""
            <div style="text-align: center; height: 50px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
                <span style="font-weight: bold; font-size: 18px; color: #34495e;">{title}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # 2. الدائرة الرقمية بتصميم CSS متطور
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 20px;">
                <div style="
                    width: 110px; 
                    height: 110px; 
                    border-radius: 50%; 
                    border: 6px solid {color}; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                    font-size: 26px; 
                    font-weight: bold;
                    color: #2c3e50;
                    background-color: #f8f9fa;
                    box-shadow: 0px 4px 15px {color}66;">
                    {val}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 3. شريط التقدم (Bar) أسفل الدائرة
        st.progress(progress_val)

# --- الرسم البياني في الأسفل ---
st.write("---")
st.subheader("📊 Live Comparative Trend")
chart_df = pd.DataFrame({
    'KPI Metrics': [k['title'] for k in kpi_configs],
    'Current Value': values
})
st.bar_chart(chart_df.set_index('KPI Metrics'))

# --- تذييل الصفحة وتوقيت التحديث ---
st.caption(f"Last updated: {time.strftime('%H:%M:%S')} - Data switches every 10 seconds.")

# آلية التكرار التلقائي
time.sleep(10)
st.session_state.index += 1
st.rerun()
