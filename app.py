import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة والتصميم (التصميم الثابت اللي طلبته)
st.set_page_config(page_title="ICU Performance Dashboard", layout="wide", initial_sidebar_state="collapsed")

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
    .census-box-mini { background: #0a0a0a; border: 2px solid #FFD700; border-radius: 12px; padding: 10px 20px; text-align: left; margin-bottom: 15px; }
    .census-num-mini { color: #FFD700; font-size: 38px; font-weight: 900; }
    .side-header { color: #00d4ff; font-size: 26px; font-weight: 900; margin-bottom: 15px; text-transform: uppercase; }
    .gauge-label-bottom { color: #ffffff; font-size: 14px; font-weight: 900; text-transform: uppercase; margin-top: -20px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. الداتا المستخرجة من ملف الدمام (3FGW-Dammam)
if 'step' not in st.session_state: st.session_state.step = 0

dammam_data = [
    {
        "q": "1Q 2024",
        "sq": [0.42, 0.00, 4.38, 0.00, 0.00, 0.00], "sq_bm": [0.35, 0.12, 7.38, 1.25, 0.88, 1.34],
        "cir": [0.00, 0.00, 6.47, 85.00, 0.00], "cir_bm": [0.11, 0.04, 7.00, 78.50, 0.15]
    },
    {
        "q": "2Q 2024",
        "sq": [0.00, 0.00, 6.41, 2.01, 0.00, 0.00], "sq_bm": [0.64, 0.00, 7.38, 1.30, 0.90, 1.40],
        "cir": [2.00, 0.00, 7.15, 82.00, 0.11], "cir_bm": [0.35, 0.02, 6.80, 80.00, 0.10]
    },
    {
        "q": "3Q 2024",
        "sq": [1.12, 0.17, 4.52, 0.00, 3.33, 0.00], "sq_bm": [0.45, 0.00, 6.41, 1.15, 0.75, 1.20],
        "cir": [9.00, 0.01, 4.79, 75.00, 0.00], "cir_bm": [0.37, 0.00, 7.10, 83.00, 0.12]
    },
    {
        "q": "4Q 2024",
        "sq": [2.09, 0.00, 3.33, 0.00, 7.15, 0.00], "sq_bm": [0.35, 0.08, 4.52, 1.10, 0.80, 1.25],
        "cir": [0.00, 0.01, 7.02, 88.00, 0.01], "cir_bm": [0.37, 0.02, 7.00, 85.00, 0.05]
    },
    {
        "q": "3Q 2025",
        "sq": [0.10, 0.00, 6.89, 0.00, 7.40, 0.00], "sq_bm": [0.43, 0.10, 3.33, 1.20, 0.85, 1.30],
        "cir": [4.00, 0.01, 6.89, 90.00, 0.00], "cir_bm": [0.40, 0.01, 7.15, 84.00, 0.08]
    }
]

device_weeks = [
    {"w": "Week 1", "census": 20, "occ": "70%", "vals": [10, 14, 3, 4.0]},
    {"w": "Week 2", "census": 24, "occ": "85%", "vals": [12, 16, 5, 4.2]},
    {"w": "Week 3", "census": 22, "occ": "78%", "vals": [11, 15, 4, 3.8]}
]

cur_q = dammam_data[st.session_state.step % len(dammam_data)]
cur_d = device_weeks[st.session_state.step % len(device_weeks)]

# --- العرض العلوي (Dammam PDF Data) ---
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 50px; font-weight:900;'>3FGW-DAMMAM PERFORMANCE</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #FFD700; font-size: 22px; font-weight:bold;'>PERIOD: {cur_q['q']}</p>", unsafe_allow_html=True)

sq_names = ["Falls", "Injury Falls", "HAPI %", "CLABSI", "CAUTI", "VAE Rate"]
c1 = st.columns(6)
for i in range(6):
    v, b = cur_q['sq'][i], cur_q['sq_bm'][i]
    color = "#00ffaa" if v <= b else "#ff4b4b"
    with c1[i]:
        st.markdown(f'<div class="kpi-card"><div class="content-box"><div class="label-full">{sq_names[i]}</div><div class="val-full" style="color:{color}">{v}</div><div class="bm-full">BENCHMARK: {b}</div></div></div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
cir_names = ["Assault Rate", "Injury Assault", "Nursing Hr", "RN Education", "C-Diff"]
c2 = st.columns(5)
for i in range(5):
    v, b = cur_q['cir'][i], cur_q['cir_bm'][i]
    # التحقق من نوع المؤشر (إيجابي أم سلبي)
    is_positive = "Education" in cir_names[i] or "Nursing Hr" in cir_names[i]
    color = "#00ffaa" if (v >= b if is_positive else v <= b) else "#ff4b4b"
    with c2[i]:
        st.markdown(f'<div class="circle-container"><div class="content-box"><div class="label-full" style="font-size:18px;">{cir_names[i]}</div><div class="val-full" style="color:{color}; font-size:42px;">{v}</div><div class="bm-full">BENCHMARK: {b}</div></div></div>', unsafe_allow_html=True)

st.markdown("<hr style='border-color:#222; margin:40px 0;'>", unsafe_allow_html=True)

# --- العرض السفلي (حركة أسبوعية مستقلة) ---
col_l, col_r = st.columns([2.2, 1.8])
with col_l:
    s1, s2 = st.columns(2)
    with s1: st.markdown(f'<div class="census-box-mini"><div style="color:#555; font-size:12px; font-weight:bold;">CURRENT CENSUS</div><div class="census-num-mini">{cur_d["census"]}</div></div>', unsafe_allow_html=True)
    with s2: st.markdown(f'<div class="census-box-mini" style="border-color:#00d4ff;"><div style="color:#555; font-size:12px; font-weight:bold;">OCCUPANCY RATE</div><div class="census-num-mini" style="color:#00d4ff;">{cur_d["occ"]}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="side-header">ATTACHED DEVICES <span style="color:#FFD700; font-size:16px;">({cur_d["w"]})</span></div>', unsafe_allow_html=True)
    g_cols = st.columns(4)
    dev_info = [("Pt with ETT", 30, [8, 15]), ("Pt with Foley", 30, [20, 25]), ("Pt with CVC", 30, [10, 20]), ("Avg Stay", 10, [4, 6])]
    for i, (n, mx, stps) in enumerate(dev_info):
        with g_cols[i]:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=cur_d['vals'][i], number={'font':{'size':35,'color':'#fff'}},
                gauge={'axis':{'range':[None,mx],'tickvals':[]},'bar':{'color':"#222"},'bgcolor':"#000",
                'steps':[{'range':[0,stps[0]],'color':"#00ffaa"},{'range':[stps[0],stps[1]],'color':"#FFD700"},{'range':[stps[1],mx],'color':"#ff4b4b"}]}))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10,b=0,l=10,r=10), height=120)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
            st.markdown(f'<div class="gauge-label-bottom">{n}</div>', unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="side-header" style="margin-left:20px;">TREND ANALYSIS</div>', unsafe_allow_html=True)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=sq_names, y=cur_q['sq'], name="Unit", marker_color='#00d4ff', text=cur_q['sq'], textposition='outside'))
    fig_bar.add_trace(go.Bar(x=sq_names, y=cur_q['sq_bm'], name="Mean", marker_color='#1a1a1a'))
    fig_bar.update_layout(height=400, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20,b=20,l=0,r=0), legend=dict(font=dict(color="#888"), orientation="h", y=1.2))
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar':False})

time.sleep(15)
st.session_state.step += 1
st.rerun()
