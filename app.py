import streamlit as st
import pandas as pd
import time

# إعدادات الصفحة (الوضع العريض)
st.set_page_config(page_title="AI ICU Command Center", layout="wide", initial_sidebar_state="collapsed")

# 1. تعريف البيانات
kpi_configs = [
    {"title": "FALLS RATE", "max": 2.0},
    {"title": "HAPI INDEX", "max": 30.0},
    {"title": "CLABSI", "max": 5.0},
    {"title": "VAE EVENTS", "max": 7.0},
    {"title": "TURNOVER", "max": 10.0}
]

quarterly_data = [
    [0.00, 26.67, 1.10, 1.05, 1.40],
    [0.24, 6.45, 2.67, 2.42, 4.34],
    [0.24, 14.29, 2.42, 0.00, 6.25],
    [0.36, 6.90, 2.63, 1.40, 4.69],
    [0.00, 9.68, 1.10, 1.40, 1.35]
]
quarters = ["4Q 2023", "1Q 2024", "2Q 2024", "3Q 2024", "4Q 2024"]

# --- CSS متقدم للمسة الـ AI (Neon & Glassmorphism) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .main-container {
        background-color: #0E1117;
        color: #00f2ff;
        font-family: 'Orbitron', sans-serif;
    }
    .ai-title {
        text-align: center;
        font-size: 50px;
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #00f2ff, #0066ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 242, 255, 0.5);
        margin-bottom: 5px;
    }
    .ai-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
    }
    .ai-circle {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        margin: 0 auto 15px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-weight: bold;
        color: #fff;
        position: relative;
        /* تأثير التوهج */
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3), inset 0 0 15px rgba(0, 242, 255, 0.2);
        border: 2px solid rgba(0, 242, 255, 0.5);
    }
    .ai-circle::after {
        content: '';
        position: absolute;
        width: 145px;
        height: 145px;
        border-radius: 50%;
        border: 2px dashed rgba(0, 242, 255, 0.4);
        animation: rotate 10s linear infinite;
    }
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    .kpi-label {
        font-size: 12px;
        letter-spacing: 2px;
        color: #8892b0;
        margin-bottom: 15px;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<p class="ai-title">ICU AI COMMAND CENTER</p>', unsafe_allow_html=True)
period_placeholder = st.empty()

st.write("---")

# إنشاء الأعمدة
cols = st.columns(len(kpi_configs))
slots = [c.empty() for c in cols]

# حلقة التحديث التلقائي
idx = 0
while True:
    current_values = quarterly_data[idx % len(quarterly_data)]
    current_q = quarters[idx % len(quarters)]
    
    # تحديث الفترة الزمنية بتنسيق AI
    period_placeholder.markdown(f"""
        <p style='text-align: center; color: #8892b0; font-family: "Orbitron";'>
            SYSTEM STATUS: <span style='color: #00f2ff;'>ACTIVE</span> | 
            DATA STREAM: <span style='color: #00f2ff;'>{current_q}</span>
        </p>
    """, unsafe_allow_html=True)
    
    for i, slot in enumerate(slots):
        val = current_values[i]
        max_val = kpi_configs[i]["max"]
        title = kpi_configs[i]["title"]
        
        # حساب النسبة للبار
        ratio = min(val / max_val, 1.0)
        # لون التوهج (أزرق ذكاء اصطناعي، أحمر للتحذير)
        glow_color = "#00f2ff" if ratio < 0.6 else "#ff0055"
        
        with slot.container():
            st.markdown(f"""
                <div class="ai-card">
                    <div class="kpi-label">{title}</div>
                    <div class="ai-circle" style="border-color: {glow_color}; box-shadow: 0 0 20px {glow_color}66;">
                        {val}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            # بار صغير تحت الدائرة يتناسب مع اللون
            st.progress(ratio)
            
    idx += 1
    time.sleep(10)
