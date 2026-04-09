import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Executive Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المطور - حركة الموسيقى في كل العناصر
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* القاعدة الأساسية لكل العناصر المتحركة */
    .music-motion {
        position: relative; background-color: #0a0a0a; overflow: hidden;
        border: 2px solid #1a1a1a; display: flex; flex-direction: column; 
        justify-content: center; text-align: center;
    }

    /* أنيميشن حركة الموسيقى */
    .music-motion::before {
        content: ''; position: absolute; width: 280%; height: 280%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }

    /* الغطاء الداخلي لإنشاء تأثير الحدود الرفيعة */
    .music-motion::after {
        content: ''; position: absolute; background-color: #0a0a0a; z-index: 1;
    }

    /* تخصيص المربعات العلوية */
    .kpi-card { height: 260px; border-radius: 20px; margin-bottom: 20px; }
    .kpi-card::after { inset: 5px; border-radius: 16px; }

    /* تخصيص الدوائر الستة */
    .circle-container { width: 220px; height: 220px; border-radius: 50%; margin: auto; }
    .circle-container::after { inset: 8px; border-radius: 50%; }

    /* تخصيص المربعات الذهبية السفلية */
    .census-card { height: 100px; border-radius: 12px; margin-bottom: 15px; border-color: #FFD700 !important; }
    .census-card::before { background: conic-gradient(#FFD700, #000, #FFD700) !important; }
    .census-card::after { inset: 4px; border-radius: 10px; }

    @keyframes rotate-wave { 0% { transform: translate(-50%, -50%) rotate(0deg); } 100% { transform: translate(-50%, -50%) rotate(360deg); } }
    
    .content-box { position: relative; z-index: 10; width: 100%; padding: 10px; }
    .label-full { color: #aaaaaa; font-size: 18px; font-weight: 900; text-transform: uppercase; }
    .val-full { color: #00d4ff; font-size: 45px; font-weight: 900; line-height: 1; }
    .bm-full { color: #444444; font-size: 12px; font-weight: bold; margin-top: 5px; }
    
    .census-num-mini { color: #FFD700; font-size: 32px; font-weight: 900; }
    .side-header { color: #00d4ff; font-size: 24px; font-weight: 900; margin-bottom: 15px; }
    .gauge-label-bottom { color: #ffffff; font-size: 13px; font-weight: 900; text-transform: uppercase; text-align: center; margin-top: -15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة حركة البيانات
if 'step' not in st.session_state: st.session_state.step = 0

pdf_quarters = [
    {"q": "3Q 2024", "sq": [0.36, 0.36, 6.90, 2.63, 1.02, 0.00], "sq_bm": [0.28, 0.05, 4.60, 1.20, 0.40, 1.89],
     "cir": [20.69, 0.00, 4.69, 12.54, 68.25, 0.00], "cir_bm": [6.32, 1.89, 4.51, 19.20, 83.36, 0.25]},
    {"q": "1Q 2025", "sq": [1.59, 0.80, 4.17, 3.02, 0.00, 6.69], "sq_bm": [0.12, 0.03, 4.96, 1.26, 0.43, 1.91],
     "cir": [12.50, 6.69, 1.43, 12.87, 70.00, 0.00], "cir_bm": [8.23, 1.91, 3.97, 19.15, 83.78, 0.26]}
]

device_weeks = [
    {"w": "Week 1", "census": 23, "occ": "78%", "vals": [12, 16, 4, 3.5]},
    {"w": "Week 2", "census": 28, "occ": "93%", "vals": [11, 15, 6, 4.5]}
]

cur_pdf = pdf_quarters[st.session_state.step % len(pdf_quarters)]
cur_dev = device_weeks[st.session_state.step % len(device_weeks)]

# الهيدر
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 45px; font-weight:900; margin:0;'>ICU PERFORMANCE TRACKER</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #FFD700; font-size: 18px; margin-bottom:20px;'>REPORTING PERIOD: {cur_pdf['q']}</p>", unsafe_allow_html=True)

# المربعات العلوية (6)
sq_names = ["Falls", "Injury Falls", "HAPI %", "CLABSI", "CAUTI", "VAE Rate"]
c1 = st.columns(6)
for i in range(6):
    v, b = cur_pdf['sq'][i], cur_pdf['sq_bm'][i]
    color = "#00ffaa" if v <= b else "#ff4b4b"
    with c1[i]:
        st.markdown(f'''<div class="music-motion kpi-card"><div class="content-box"><div class="label-full">{sq_names[i]}</div><div class="val-full" style="color:{color}">{v}</div><div class="bm-full">BM: {b}</div></div></div>''', unsafe_allow_html=True)

# الدوائر الوسطى (6)
cir_names = ["Restraints", "VAE Rate", "Turnover", "Nurse Hr", "RN Edu", "C-Diff"]
c2 = st.columns(6)
for i in range(6):
    v, b = cur_pdf['cir'][i], cur_pdf['cir_bm'][i]
    is_rev = any(x in cir_names[i] for x in ["Hr", "Edu"])
    color = "#00ffaa" if (v >= b if is_rev else v <= b) else "#ff4b4b"
    with c2[i]:
        st.markdown(f'''<div class="music-motion circle-container"><div class="content-box"><div class="label-full" style="font-size:14px;">{cir_names[i]}</div><div style="color:{color}; font-size:38px; font-weight:900;">{v}</div><div class="bm-full" style="font-size:10px;">BM: {b}</div></div></div>''', unsafe_allow_html=True)

st.markdown("<hr style='border-color:#222; margin:30px 0;'>", unsafe_allow_html=True)

# الجزء السفلي
col_left, col_right = st.columns([2.2, 1.8])

with col_left:
    sub_c1, sub_c2 = st.columns(2)
    with sub_c1:
        st.markdown(f'''<div class="music-motion census-card"><div class="content-box"><div style="color:#888; font-size:12px;">CENSUS</div><div class="census-num-mini">{cur_dev["census"]}</div></div></div>''', unsafe_allow_html=True)
    with sub_c2:
        st.markdown(f'''<div class="music-motion census-card" style="border-color:#00d4ff !important;"><div class="content-box"><div style="color:#888; font-size:12px;">OCCUPANCY</div><div class="census-num-mini" style="color:#00d4ff;">{cur_dev["occ"]}</div></div></div>''', unsafe_allow_html=True)
    
    st.markdown(f'<div class="side-header">ATTACHED DEVICES <span style="color:#FFD700; font-size:14px;">({cur_dev["w"]})</span></div>', unsafe_allow_html=True)
    
    g_cols = st.columns(4)
    dev_info = [("ETT", 36, [10, 18]), ("Foley", 36, [24, 30]), ("CVC", 36, [16, 22]), ("LOS", 10, [4, 6])]
    for i, (name, mx, steps) in enumerate(dev_info):
        with g_cols[i]:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = cur_dev['vals'][i],
                number = {'font': {'size': 25, 'color': '#fff'}},
                gauge = {'axis': {'range': [None, mx], 'tickvals': []}, 'bar': {'color': "#00d4ff"}, 'bgcolor': "#000",
                         'steps': [{'range': [0, steps[0]], 'color': "#00ffaa"}, {'range': [steps[0], steps[1]], 'color': "#FFD700"}, {'range': [steps[1], mx], 'color': "#ff4b4b"}]}
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=10, r=10), height=100)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<div class="gauge-label-bottom">{name}</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="side-header">QUARTERLY ANALYTICS</div>', unsafe_allow_html=True)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=sq_names, y=cur_pdf['sq'], name="Current", marker_color='#00d4ff'))
    fig_bar.add_trace(go.Bar(x=sq_names, y=cur_pdf['sq_bm'], name="Benchmark", marker_color='#333'))
    fig_bar.update_layout(height=350, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          margin=dict(t=10, b=10, l=0, r=0), legend=dict(font=dict(color="#888"), orientation="h", y=1.1))
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

time.sleep(15)
st.session_state.step += 1
st.rerun()
