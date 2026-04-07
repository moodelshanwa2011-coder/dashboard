import streamlit as st
import pandas as pd
import time

# إعدادات الصفحة
st.set_page_config(page_title="ICU Elite Dashboard", layout="wide")

# 1. تعريف الـ KPIs مع قيم مستهدفة (Target) للمقارنة
kpi_configs = [
    {"title": "Falls Rate", "max": 2.0},
    {"title": "Pressure Injuries", "max": 30.0},
    {"title": "CLABSI Rate", "max": 5.0},
    {"title": "VAE Rate", "max": 7.0},
    {"title": "Nurse Turnover", "max": 10.0}
]

# 2. البيانات (التي ستتغير بانسيابية)
quarterly_data = [
    [0.00, 26.67, 1.10, 1.05, 1.40],
    [0.24, 6.45, 2.67, 2.42, 4.34],
    [0.24, 14.29, 2.42, 0.00, 6.25],
    [0.36, 6.90, 2.63, 1.40, 4.69],
    [0.00, 9.68, 1.10, 1.40, 1.35]
]
quarters = ["4Q 2023", "1Q 2024", "2Q 2024", "3Q 2024", "4Q 2024"]

# --- تنسيق العنوان الكبير في المنتصف ---
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 45px;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 5px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .sub-title {
        text-align: center;
        font-size: 20px;
        color: #64748B;
        margin-bottom: 40px;
    }
    .kpi-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .circle-container {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin: 0 auto 15px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        color: #1E293B;
        border: 8px solid #F1F5F9;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">ICU PERFORMANCE INTELLIGENCE</p>', unsafe_allow_html=True)
period_display = st.empty() # مكان مخصص لتحديث اسم الفترة

st.write("---")

# إنشاء حاويات فارغة (Placeholders) لتحديث المحتوى بداخلها فقط دون الصفحة
placeholders = st.columns(len(kpi_configs))
kpi_slots = [p.empty() for p in placeholders]

# حلقة التكرار اللانهائية للعرض التفاعلي
idx = 0
while True:
    current_values = quarterly_data[idx % len(quarterly_data)]
    current_q = quarters[idx % len(quarters)]
    
    # تحديث اسم الفترة في الأعلى
    period_display.markdown(f'<p class="sub-title">Live Monitoring: <span style="color:#3B82F6; font-weight:bold;">{current_q}</span></p>', unsafe_allow_html=True)
    
    for i, slot in enumerate(kpi_slots):
        val = current_values[i]
        max_val = kpi_configs[i]["max"]
        title = kpi_configs[i]["title"]
        
        # تحديد اللون بناءً على النسبة
        ratio = val / max_val
        color = "#10B981" if ratio < 0.4 else "#F59E0B" if ratio < 0.7 else "#EF4444"
        
        # تحديث "محتوى" العمود فقط
        with slot.container():
            st.markdown(f"""
                <div class="kpi-card">
                    <div style="font-size: 14px; font-weight: 600; color: #64748B; margin-bottom: 15px; height: 35px;">{title}</div>
                    <div class="circle-container" style="border-color: {color};">
                        {val}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            # البار يتغير أسفل الدائرة
            st.progress(min(ratio, 1.0))

    # تحديث البار تشارت في الأسفل (اختياري)
    # ملاحظة: الرسوم البيانية تعيد بناء نفسها، لكن بوضعها في حاوية empty تبدو أفضل
    
    idx += 1
    time.sleep(10) # الانتظار 10 ثواني قبل الانتقال للربع التالي
