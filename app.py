import streamlit as st
import pandas as pd
import time

# 1. إعدادات الصفحة (ثيم داكن واحترافي)
st.set_page_config(page_title="ICU AI Performance Dashboard", layout="wide")

# 2. قاعدة البيانات (مستخرجة من صورتك بدقة)
kpi_labels = ["FALLS", "HAPI", "CLABSI", "VAE", "TURNOVER"]
data_history = [
    [0.00, 26.67, 1.10, 1.05, 1.40],
    [0.24, 6.45, 2.67, 2.42, 4.34],
    [0.24, 14.29, 2.42, 0.00, 6.25],
    [0.36, 6.90, 2.63, 1.40, 4.69],
    [0.00, 9.68, 1.10, 1.40, 1.35]
]
quarters = ["4Q 2023", "1Q 2024", "2Q 2024", "3Q 2024", "4Q 2024"]

# --- تنسيق الواجهة (CSS) لمظهر الذكاء الاصطناعي ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');
    
    /* خلفية الصفحة */
    .stApp { background-color: #0B1015; color: white; }
    
    /* العنوان الكبير في المنتصف */
    .main-title { 
        text-align: center; 
        font-family: 'Orbitron', sans-serif; 
        color: #00f2ff; 
        font-size: 38px; 
        font-weight: bold;
        margin-top: -20px;
        text-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
    }
    
    /* كروت الـ KPIs (الدوائر المطورة) */
    .kpi-card { 
        background: rgba(0, 242, 255, 0.05); 
        border: 1px solid rgba(0, 242, 255, 0.3); 
        border-radius: 15px; 
        padding: 20px; 
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .kpi-value { 
        font-family: 'Orbitron', sans-serif; 
        font-size: 28px; 
        color: #fff; 
        margin: 10px 0;
        text-shadow: 0 0 10px #00f2ff;
    }
    
    .kpi-label { 
        font-size: 12px; 
        color: #8B949E; 
        text-transform: uppercase; 
        letter-spacing: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# --- الهيكل الرئيسي ---

# 1. العنوان الرئيسي
st.markdown('<div class="main-title">ICU PERFORMANCE COMMAND CENTER</div>', unsafe_allow_html=True)

# إدارة العداد (Session State) لتحديث البيانات تلقائياً
if 'step' not in st.session_state:
    st.session_state.step = 0

# جلب بيانات الدورة الحالية
idx = st.session_state.step % len(data_history)
current_vals = data_history[idx]
current_q = quarters[idx]

# عرض الفترة الزمنية في المنتصف
st.markdown(f"<p style='text-align: center; color: #8B949E; font-family: Orbitron; margin-bottom: 30px;'>SYSTEM STATUS: ACTIVE | PERIOD: <span style='color: #00f2ff;'>{current_q}</span></p>", unsafe_allow_html=True)

# 2. عرض كروت الـ KPIs (التي طلبتها كدوائر متقدمة)
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{kpi_labels[i]}</div>
                <div class="kpi-value">{current_vals[i]}</div>
            </div>
        """, unsafe_allow_html=True)

st.write("---")

# 3. عرض البار تشارت (تلقائي، سمباتيك، وبدون أخطاء)
# استخدام أعمدة جانبية (Spacers) لجعل البار في المنتصف بمساحة أنيقة
left_space, center_plot, right_space = st.columns([0.7, 2, 0.7])

with center_plot:
    # تحويل البيانات لجدول ليفهمه المتصفح
    df_plot = pd.DataFrame({
        'Metric': kpi_labels,
        'Performance': current_vals
    }).set_index('Metric')
    
    # استخدام الرسم البياني الأصلي لـ Streamlit لضمان الاستقرار التام وظهور المحاور
    st.bar_chart(df_plot, color="#00f2ff", use_container_width=True)

# --- منطق التحديث التلقائي ---
# الانتظار 10 ثوانٍ ثم إعادة تحميل الصفحة بالبيانات الجديدة
time.sleep(10)
st.session_state.step += 1
st.rerun()
