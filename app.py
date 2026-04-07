import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Advanced Command Center", layout="wide")

# 2. البيانات (8 مؤشرات من ملف الرياض)
kpi_labels = ['FALLS RATE', 'HAPI INDEX', 'CLABSI', 'VAE EVENTS', 'CAUTI', 'RN BSN %', 'TURNOVER', 'NURSING HRS']
data_history = [
    [0.00, 26.67, 1.10, 1.05, 0.46, 83.53, 1.60, 19.09],
    [0.24, 6.45, 2.67, 2.42, 0.99, 70.31, 4.49, 12.54],
    [0.24, 14.29, 2.42, 0.00, 0.51, 71.21, 6.25, 19.20],
    [0.36, 6.90, 2.63, 1.40, 1.02, 82.74, 4.69, 12.39],
    [0.00, 9.68, 1.10, 1.40, 1.13, 83.36, 1.35, 19.82]
]
quarters = ["4Q 2023", "1Q 2024", "2Q 2024", "3Q 2024", "4Q 2024"]

# --- CSS التنسيق (تكبير الدوائر والكبسولات) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background-color: #05070A; color: white; }
    
    .main-title {
        text-align: center; font-family: 'Orbitron'; font-size: 32px;
        background: linear-gradient(90deg, #00f2ff, #7000ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 20px; font-weight: bold;
    }
    
    /* تكبير الكبسولات (الدوائر المطورة) */
    .big-kpi-card {
        background: rgba(0, 242, 255, 0.03);
        border: 2px solid rgba(0, 242, 255, 0.2);
        border-radius: 20px; padding: 25px 10px; text-align: center;
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
        margin-bottom: 10px;
    }
    .big-val { font-family: 'Orbitron'; font-size: 30px; color: #00f2ff; text-shadow: 0 0 10px #00f2ff; }
    .big-label { font-size: 11px; color: #8B949E; letter-spacing: 1px; font-weight: bold; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">ICU AI COMMAND CENTER</p>', unsafe_allow_html=True)

# إدارة العداد
if 'step' not in st.session_state: st.session_state.step = 0
idx = st.session_state.step % len(data_history)
vals = data_history[idx]

st.markdown(f"<p style='text-align:center; font-family:Orbitron; color:#444;'>PERIOD: <span style='color:#7000ff;'>{quarters[idx]}</span></p>", unsafe_allow_html=True)

# 3. عرض الـ 8 مؤشرات بكبسولات كبيرة (صفين في 4 أعمدة)
row1 = st.columns(4)
row2 = st.columns(4)
all_cols = row1 + row2

for i in range(8):
    all_cols[i].markdown(f"""
        <div class="big-kpi-card">
            <div class="big-label">{kpi_labels[i]}</div>
            <div class="big-val">{vals[i]}</div>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# 4. البار تشارت بالعرض (Horizontal Bar Chart)
_, center_col, _ = st.columns([0.3, 2, 0.3])
with center_col:
    fig = go.Figure(go.Bar(
        x=vals,
        y=kpi_labels,
        orientation='h', # هذا يجعل البار بالعرض
        marker=dict(
            color=vals,
            colorscale=[[0, '#7000ff'], [1, '#00f2ff']],
            line=dict(color='#fff', width=0.5)
        ),
        text=vals,
        textposition='outside',
        textfont=dict(color='#fff', family='Orbitron')
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500,
        margin=dict(l=150, r=50, t=20, b=20), # هوامش لأسماء المؤشرات الطويلة
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#8B949E', family='Orbitron')),
        yaxis=dict(tickfont=dict(color='#00f2ff', family='Orbitron', size=11), autorange="reversed"), # عكس الترتيب ليطابق الجدول
        showlegend=False
    )

    # عرض الشارت باستخدام Key ديناميكي لمنع الـ Error
    st.plotly_chart(fig, use_container_width=True, key=f"hbar_{st.session_state.step}")

# التحديث التلقائي
time.sleep(10)
st.session_state.step += 1
st.rerun()
