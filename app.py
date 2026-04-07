import streamlit as st
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

# --- CSS لمظهر الـ AI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');
    .stApp { background-color: #0B1015; color: white; }
    .ai-title { text-align: center; font-family: 'Orbitron'; color: #00f2ff; font-size: 30px; margin-bottom: 20px; }
    .kpi-box { 
        background: #161B22; border-bottom: 3px solid #00f2ff; border-radius: 10px; 
        padding: 20px; text-align: center; height: 120px;
    }
    .val-text { font-family: 'Orbitron'; font-size: 26px; color: #fff; font-weight: bold; }
    .label-text { font-size: 11px; color: #8B949E; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="ai-title">ICU COMMAND CENTER</p>', unsafe_allow_html=True)

# إدارة العداد
if 'step' not in st.session_state:
    st.session_state.step = 0

idx = st.session_state.step % len(data_history)
vals = data_history[idx]
q_name = quarters[idx]

st.markdown(f"<p style='text-align:center; color:#8B949E; font-family:Orbitron;'>PERIOD: {q_name}</p>", unsafe_allow_html=True)

# 3. عرض الكروت (بديلة الدوائر - مستقرة جداً)
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        st.markdown(f"""
            <div class="kpi-box">
                <div class="label-text">{kpi_labels[i]}</div>
                <div class="val-text">{vals[i]}</div>
            </div>
        """, unsafe_allow_html=True)

st.write("---")

# 4. البار تشارت "السمباتيك" (باستخدام أعمدة Streamlit الأصلية)
# هذا الجزء مستحيل يظهر فيه ValueError لأنه لا يستخدم Plotly
st.markdown("<p style='text-align:center; color:#00f2ff; font-family:Orbitron; font-size:14px;'>PERFORMANCE VISUALIZER</p>", unsafe_allow_html=True)

_, center_col, _ = st.columns([1, 2, 1])

with center_col:
    for i in range(5):
        # حساب النسبة المئوية للبار (بافتراض أقصى قيمة 30)
        progress_val = min(vals[i] / 30.0, 1.0) 
        st.write(f"**{kpi_labels[i]}**: {vals[i]}")
        st.progress(progress_val)

# 5. التحديث التلقائي
time.sleep(10)
st.session_state.step += 1
st.rerun()
