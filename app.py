import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المعتمد - حدود نيون قوية وتنسيق احترافي
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    .kpi-card {
        position: relative; background-color: #0a0a0a; border-radius: 20px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; height: 260px; margin-bottom: 20px;
        border: 2px solid #1a1a1a; box-shadow: 0 0 20px rgba(0, 212, 255, 0.2); 
    }
    .kpi-card::before, .circle-container::before {
        content: ''; position: absolute; width: 250%; height: 250%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }
    .kpi-card::after, .circle-container::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 5px; border-radius: 16px;
    }
    
    .circle-container {
        position: relative; width: 280px; height: 280px; border-radius: 50%;
        margin: auto; overflow: hidden; display: flex; justify-content: center; align-items: center; text-align: center;
        border: 2px solid #1a1a1a; box-shadow: 0 0 25px rgba(0, 212, 255, 0.25);
    }
    .circle-container::after { border-radius: 50%; inset: 10px; }
    
    @keyframes rotate-wave { 0% { transform: translate(-50%, -50%) rotate(0deg); } 100% { transform: translate(-50%, -50%) rotate(360deg); } }
    
    .content-box { position: relative; z-index: 10; width: 100%; padding: 10px; }
    .label-full { color: #aaaaaa; font-size: 20px; font-weight: 900; text-transform: uppercase; margin-bottom: 5px; }
    .val-full { color: #00d4ff; font-size: 48px; font-weight: 900; line-height: 1; }
    .bm-full { color: #444444; font-size: 13px; font-weight: bold; margin-top: 10px; text-transform: uppercase; }

    .census-box-mini { 
        background: #0a0a0a; border: 2px solid #FFD700; border-radius: 12px; 
        padding: 10px 20px; text-align: left; margin-bottom: 15px;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.1);
    }
    .census-num-mini { color: #FFD700; font-size: 38px; font-weight: 900; }
    .side-header { color: #00d4ff; font-size: 26px; font-weight: 900; margin-bottom: 15px; text-transform: uppercase; }
    .gauge-label-bottom { color: #ffffff; font-size: 14px; font-weight: 900; text-transform: uppercase; margin-top: -20px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. داتا الـ PDF الشاملة (جميع الأعمدة من الملف)
if 'step' not in st.session_state: st.session_state.step = 0

pdf_data = [
    {
        "q": "4Q 2023",
        "sq": [0, 0, 0, 0.58, 0, 0], 
        "sq_bm": [0.04, 0.03, 3.48, 1.25, 0.53, 1.84],
        "cir": [5.21, 0, 1.60, 11.52, 83.53, 0],
        "cir_bm": [4.49, 1.84, 4.84, 16.71, 67.19, 0.21]
    },
    {
        "q": "1Q 2024",
        "sq": [0.24, 0, 5.14, 0.81, 0, 0.96],
        "sq_bm": [0.09, 0.04, 4.29, 1.15, 0.44, 1.87],
        "cir": [6.25, 0.96, 4.49, 10.15, 82.99, 0],
        "cir_bm": [3.74, 1.87, 4.84, 18.06, 71.21, 0.22]
    },
    {
        "q": "3Q 2024",
        "sq": [0.36, 0.36, 6.90, 2.63, 1.02, 0],
        "sq_bm": [0.28, 0.05, 4.60, 1.20, 0.40, 1.89],
        "cir": [4.69, 0, 4.35, 12.54, 68.25, 0],
        "cir_bm": [4.51, 1.89, 4.16, 19.20, 83.36, 0.25]
    },
    {
        "q": "4Q 2024",
        "sq": [0, 0, 9.68, 1.80, 1.13, 1.60],
        "sq_bm": [0.14, 0.01, 4.61, 1.21, 0.54, 2.49],
        "cir": [4.35, 1.60, 1.43, 12.39, 71.83, 0],
        "cir_bm": [4.16, 2.49, 3.97, 19.82, 83.30, 0.11]
    },
    {
        "q": "1Q 2025",
        "sq": [1.59, 0.80, 4.17, 3.02, 0, 6.69],
        "sq_bm": [0.12, 0.03, 4.96, 1.26, 0.43, 1.91],
        "cir": [1.43, 6.69, 2.90, 12.87, 70.00, 0],
        "cir_bm": [3.97, 1.91, 3.22, 19.15, 83.78, 0.26]
    },
    {
        "q": "2Q 2025",
        "sq": [0.18, 0.04, 4.58, 3.38, 0.44, 3.40],
        "sq_bm": [0, 0, 6.67, 1.50, 0, 1.60],
        "cir": [2.90, 3.40, 0, 19.26, 70.59, 0.45],
        "cir_bm": [3.22, 1.60, 0, 13.00, 85.01, 0]
    }
]

device_weeks = [
    {"w": "Week 1", "census": 23, "occ": "78%", "vals": [12, 16, 4, 3.5]},
    {"w": "Week 2", "census": 28, "occ": "93%", "vals": [11, 15, 6, 4.5]},
    {"w": "Week 3", "census": 25, "occ": "85%", "vals": [13, 18, 5, 4.2]}
]

cur_pdf = pdf_data[st.session_state.step % len(pdf_data)]
cur_dev = device_weeks[st.session_state.step % len(device_weeks)]

# --- العنوان ---
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 50px; font-weight:900;'>ICU PERFORMANCE DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #FFD700; font-size: 22px; font-weight:bold;'>QUARTERLY DATA: {cur_pdf['q']}</p>", unsafe_allow_html=True)

# الصف 1: المربعات (Falls to VAE)
sq_labels = ["Falls", "Injury Falls", "HAPI %", "CLABSI", "CAUTI", "VAE Rate"]
c1 = st.columns(6)
for i in range(6):
    v, b = cur_pdf['sq'][i], cur_pdf['sq_bm'][i]
    color = "#00ffaa" if v <= b else "#ff4b4b"
    with c1[i]:
        st.markdown(f'<div class="kpi-card"><div class="content-box"><div class="label-full">{sq_labels[i]}</div><div class="val-full" style="color:{color}">{v}</div><div class="bm-full">BENCHMARK: {b}</div></div></div>', unsafe_allow_html=True)

# الصف 2: الدوائر (Turnover, Education, Restraints etc.)
cir_labels = ["Turnover", "VAE Rate", "Restraints", "Nurse Hr", "RN Education", "C-Diff"]
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
c2 = st.columns(6)
for i in range(6):
    v, b = cur_pdf['cir'][i], cur_pdf['cir_bm'][i]
    is_positive = "Education" in cir_labels[i] or "Nurse Hr" in cir_labels[i]
    color = "#00ffaa" if (v >= b if is_positive else v <= b) else "#ff4b4b"
    with c2[i]:
        st.markdown(f'<div class="circle-container"><div class="content-box"><div class="label-full" style="font-size:18px;">{cir_labels[i]}</div><div class="val-text" style="color:{color}; font-size:42px; font-weight:900;">{v}</div><div class="bm-full">BENCHMARK: {b}</div></div></div>', unsafe_allow_html=True)

st.markdown("<hr style='border-color:#222; margin:40px 0;'>", unsafe_allow_html=True)

# --- السفلي (Devices & Trend) ---
col_l, col_r = st.columns([2.2, 1.8])

with col_l:
    s1, s2 = st.columns(2)
    with s1: st.markdown(f'<div class="census-box-mini"><div style="color:#555; font-size:12px; font-weight:bold;">CURRENT CENSUS</div><div class="census-num-mini">{cur_dev["census"]}</div></div>', unsafe_allow_html=True)
    with s2: st.markdown(f'<div class="census-box-mini" style="border-color:#00d4ff;"><div style="color:#555; font-size:12px; font-weight:bold;">OCCUPANCY RATE</div><div class="census-num-mini" style="color:#00d4ff;">{cur_dev["occ"]}</div></div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="side-header">ATTACHED DEVICES <span style="color:#FFD700; font-size:16px;">({cur_dev["w"]})</span></div>', unsafe_allow_html=True)
    g_cols = st.columns(4)
    dev_names = [("Pt with ETT", 36, [10, 18]), ("Pt with Foley", 36, [24, 30]), ("Pt with CVC", 36, [16, 22]), ("Avg Stay", 10, [4, 6])]
    for i, (n, mx, stps) in enumerate(dev_names):
        with g_cols[i]:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = cur_dev['vals'][i],
                number = {'font': {'size': 35, 'color': '#fff'}},
                gauge = {'axis': {'range': [None, mx], 'tickvals': []}, 'bar': {'color': "#222"}, 'bgcolor': "#000",
                         'steps': [{'range': [0, stps[0]], 'color': "#00ffaa"}, {'range': [stps[0], stps[1]], 'color': "#FFD700"}, {'range': [stps[1], mx], 'color': "#ff4b4b"}]}
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=0, l=10, r=10), height=120)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<div class="gauge-label-bottom">{n}</div>', unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="side-header" style="margin-left:20px;">TREND ANALYSIS</div>', unsafe_allow_html=True)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=sq_labels, y=cur_pdf['sq'], name="Unit", marker_color='#00d4ff', text=cur_pdf['sq'], textposition='outside'))
    fig_bar.add_trace(go.Bar(x=sq_labels, y=cur_pdf['sq_bm'], name="Mean", marker_color='#1a1a1a'))
    fig_bar.update_layout(height=400, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          margin=dict(t=20, b=20, l=0, r=0), legend=dict(font=dict(color="#888"), orientation="h", y=1.2))
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

time.sleep(15)
st.session_state.step += 1
st.rerun()
