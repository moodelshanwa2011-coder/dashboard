import streamlit as st
import plotly.graph_objects as go
import time
import random

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Riyadh Performance", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المعتمد - الحفاظ على التصميم النيون وحركة الـ Wave مع إضافة استايل الأعمدة الموسيقية
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    .kpi-card {
        position: relative; background-color: #0a0a0a; border-radius: 20px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; height: 260px; margin-bottom: 20px;
        border: 2px solid #1a1a1a; 
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2); 
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
        border: 2px solid #1a1a1a;
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.25);
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
    }
    .census-num-mini { color: #FFD700; font-size: 38px; font-weight: 900; }
    .side-header { color: #00d4ff; font-size: 26px; font-weight: 900; margin-bottom: 15px; text-transform: uppercase; }
    .gauge-label-bottom { color: #ffffff; font-size: 14px; font-weight: 900; text-transform: uppercase; margin-top: -15px; text-align: center; }

    /* استايل الأعمدة الموسيقية */
    .music-bars {
        display: flex; justify-content: center; align-items: flex-end;
        height: 20px; gap: 2px; margin-top: 5px; margin-bottom: 10px;
    }
    .bar {
        width: 3px; background-color: #00d4ff; border-radius: 1px;
        animation: music-flow 1.2s ease-in-out infinite alternate;
    }
    @keyframes music-flow {
        0% { height: 3px; opacity: 0.3; }
        100% { height: 18px; opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات والسيكل
if 'step' not in st.session_state: st.session_state.step = 0

# بيانات الأرباع (تتغير مع كل تحديث للصفحة)
pdf_data = [
    {"q": "4Q 2023", "sq": [0.00, 0.00, 7.30, 1.38, 1.57, 0.00], "sq_bm": [0.04, 0.03, 26.6, 1.30, 1.00, 0.40],
     "cir": [67.19, 5.21, 13.0, 0.21, 0.00, 0.00], "cir_bm": [83.53, 1.60, 8.00, 0.00, 0.00, 0.00]},
    {"q": "1Q 2024", "sq": [0.24, 0.00, 6.45, 1.28, 2.17, 0.70], "sq_bm": [0.09, 0.04, 7.70, 2.60, 2.40, 0.90],
     "cir": [82.99, 4.84, 20.1, 0.22, 0.00, 0.00], "cir_bm": [70.31, 4.49, 19.1, 0.00, 0.00, 0.00]}
]

# تعديل مسميات الأسابيع من March 1Wk إلى April 1Wk
device_weeks = [
    {"w": "March 1Wk", "census": 24, "occ": "80%", "vals": [12, 16, 5, 4.1]},
    {"w": "March 2Wk", "census": 26, "occ": "87%", "vals": [14, 15, 4, 3.8]},
    {"w": "March 3Wk", "census": 22, "occ": "73%", "vals": [11, 18, 6, 4.5]},
    {"w": "March 4Wk", "census": 25, "occ": "82%", "vals": [13, 17, 5, 4.0]},
    {"w": "April 1Wk", "census": 28, "occ": "94%", "vals": [15, 19, 7, 4.8]}
]

cur_pdf = pdf_data[st.session_state.step % len(pdf_data)]
cur_dev = device_weeks[st.session_state.step % len(device_weeks)]

# --- الجزء العلوي ---
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 50px; font-weight:900;'>ICU RIYADH PERFORMANCE</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #FFD700; font-size: 20px; font-weight:bold;'>ANALYSIS PERIOD: {cur_pdf['q']}</p>", unsafe_allow_html=True)

sq_names = ["Total Falls", "Injury Falls", "HAPI %", "CLABSI", "VAE Rate", "CAUTI"]
c1 = st.columns(6)
for i in range(6):
    v, b = cur_pdf['sq'][i], cur_pdf['sq_bm'][i]
    color = "#00ffaa" if v <= b else "#ff4b4b"
    with c1[i]:
        st.markdown(f'<div class="kpi-card"><div class="content-box"><div class="label-full">{sq_names[i]}</div><div class="val-full" style="color:{color}">{v}</div><div class="bm-full">BENCHMARK: {b}</div></div></div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

cir_names = ["RN Education", "Nurse Turnover", "Total RN Hrs", "MDRO-MRSA", "HAPI P2", "CLABSI P2"]
c2 = st.columns(6)
for i in range(6):
    v, b = cur_pdf['cir'][i], cur_pdf['cir_bm'][i]
    is_higher_better = "Education" in cir_names[i] or "RN Hrs" in cir_names[i]
    color = "#00ffaa" if (v >= b if is_higher_better else v <= b) else "#ff4b4b"
    with c2[i]:
        st.markdown(f'<div class="circle-container"><div class="content-box"><div class="label-full" style="font-size:16px;">{cir_names[i]}</div><div class="val-full" style="color:{color}; font-size:42px;">{v}</div><div class="bm-full">BENCHMARK: {b}</div></div></div>', unsafe_allow_html=True)

st.markdown("<hr style='border-color:#111; margin:40px 0;'>", unsafe_allow_html=True)

# --- الجزء السفلي ---
col_left, col_right = st.columns([2.2, 1.8])

with col_left:
    sub_c1, sub_c2 = st.columns(2)
    with sub_c1: st.markdown(f'<div class="census-box-mini"><div style="color:#555; font-size:12px; font-weight:bold;">CURRENT CENSUS</div><div class="census-num-mini">{cur_dev["census"]}</div></div>', unsafe_allow_html=True)
    with sub_c2: st.markdown(f'<div class="census-box-mini" style="border-color:#00d4ff;"><div style="color:#555; font-size:12px; font-weight:bold;">OCCUPANCY RATE</div><div class="census-num-mini" style="color:#00d4ff;">{cur_dev["occ"]}</div></div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="side-header">UNIT DEVICE UTILIZATION <span style="color:#FFD700; font-size:16px;">({cur_dev["w"]})</span></div>', unsafe_allow_html=True)
    g_cols = st.columns(4)
    dev_info = [("Pt with ETT", 30, [10, 18]), ("Pt with Foley", 30, [20, 25]), ("Pt with CVC", 30, [15, 22]), ("Avg Stay", 10, [4, 6])]
    for i, (name, mx, steps) in enumerate(dev_info):
        with g_cols[i]:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=cur_dev['vals'][i], number={'font':{'size':35,'color':'#fff'}},
                gauge={'axis':{'range':[None,mx],'tickvals':[]},'bar':{'color':"#222"},'bgcolor':"#000",
                'steps':[{'range':[0,steps[0]],'color':"#00ffaa"},{'range':[steps[0],steps[1]],'color':"#FFD700"},{'range':[steps[1],mx],'color':"#ff4b4b"}]}))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10,b=0,l=10,r=10), height=110)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
            
            # الأعمدة الموسيقية أسفل كل Gauge
            bars_html = '<div class="music-bars">' + ''.join([f'<div class="bar" style="animation-delay: {random.random()}s"></div>' for _ in range(12)]) + '</div>'
            st.markdown(bars_html, unsafe_allow_html=True)
            st.markdown(f'<div class="gauge-label-bottom">{name}</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="side-header" style="margin-left:20px;">QUARTERLY ANALYTICS</div>', unsafe_allow_html=True)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=sq_names, y=cur_pdf['sq'], name="Unit", marker_color='#00d4ff', text=cur_pdf['sq'], textposition='outside'))
    fig_bar.add_trace(go.Bar(x=sq_names, y=cur_pdf['sq_bm'], name="Mean", marker_color='#1a1a1a'))
    fig_bar.update_layout(height=400, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20,b=20,l=0,r=0), legend=dict(font=dict(color="#888"), orientation="h", y=1.2))
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar':False})

# التحديث التلقائي كل 15 ثانية لإعادة السيكل
time.sleep(15)
st.session_state.step += 1
st.rerun()
