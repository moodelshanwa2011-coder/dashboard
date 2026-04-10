import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS - التصميم المعتمد (ثابت تماماً)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    .visualizer {
        position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%);
        display: flex; gap: 4px; height: 35px; align-items: flex-end; z-index: 5; opacity: 0.7;
    }
    .v-bar { width: 4px; border-radius: 2px; animation: bounce 1s ease-in-out infinite; }
    .v-bar:nth-child(1) { background: #ff00ff; animation-delay: 0.1s; }
    .v-bar:nth-child(2) { background: #00d4ff; animation-delay: 0.3s; }
    .v-bar:nth-child(3) { background: #FFD700; animation-delay: 0.2s; }
    .v-bar:nth-child(4) { background: #00ffaa; animation-delay: 0.4s; }
    .v-bar:nth-child(5) { background: #ff4b4b; animation-delay: 0.1s; }
    @keyframes bounce { 0%, 100% { height: 30%; } 50% { height: 100%; } }

    .kpi-card, .circle-container {
        position: relative; background-color: #0a0a0a; border-radius: 20px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; border: 2px solid #1a1a1a;
    }
    .kpi-card { height: 260px; margin-bottom: 20px; }
    .circle-container { width: 280px; height: 280px; border-radius: 50%; margin: auto; }
    .kpi-card::before, .circle-container::before {
        content: ''; position: absolute; width: 250%; height: 250%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }
    .kpi-card::after, .circle-container::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 5px; border-radius: 16px;
    }
    .circle-container::after { border-radius: 50%; inset: 10px; }
    @keyframes rotate-wave { 0% { transform: translate(-50%, -50%) rotate(0deg); } 100% { transform: translate(-50%, -50%) rotate(360deg); } }
    .content-box { position: relative; z-index: 10; width: 100%; padding: 10px; }
    .label-full { color: #aaaaaa; font-size: 20px; font-weight: 900; text-transform: uppercase; }
    .val-full { color: #00d4ff; font-size: 50px; font-weight: 900; line-height: 1; }
    .bm-full { color: #444444; font-size: 14px; font-weight: bold; margin-top: 10px; text-transform: uppercase; }
    .census-box-mini { 
        position: relative; background: #0a0a0a; border: 2px solid #FFD700; border-radius: 12px; 
        padding: 10px 20px; text-align: left; margin-bottom: 15px; overflow: hidden;
    }
    .side-header { color: #00d4ff; font-size: 26px; font-weight: 900; margin-bottom: 15px; text-transform: uppercase; }
    .gauge-label-bottom { color: #ffffff; font-size: 14px; font-weight: 900; text-transform: uppercase; margin-top: -20px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

m_bars = '<div class="visualizer"><div class="v-bar"></div><div class="v-bar"></div><div class="v-bar"></div><div class="v-bar"></div><div class="v-bar"></div></div>'

# 3. إدارة البيانات - الترتيب التصاعدي
if 'step' not in st.session_state: st.session_state.step = 0

# أ) بيانات الـ Quarters (ثابتة كما طلبت)
pdf_timeline = [
    {"q": "4Q 2023", "sq": [0.00, 0.00, 3.85, 1.25, 0.50, 0.00], "sq_bm": [0.04, 0.03, 4.20, 1.15, 0.38, 1.80], "cir": [15.20, 0.00, 5.21, 10.50, 67.19, 0.00], "cir_bm": [5.50, 1.80, 4.80, 18.50, 83.53, 0.20]},
    {"q": "1Q 2024", "sq": [0.24, 0.00, 4.50, 1.10, 0.45, 0.11], "sq_bm": [0.09, 0.04, 4.30, 1.18, 0.42, 1.85], "cir": [18.40, 0.11, 4.84, 11.20, 82.99, 0.16], "cir_bm": [6.10, 1.85, 4.49, 18.90, 70.31, 0.22]},
    {"q": "2Q 2024", "sq": [0.24, 0.24, 4.10, 1.30, 0.30, 0.00], "sq_bm": [0.06, 0.01, 4.40, 1.22, 0.35, 1.82], "cir": [16.80, 0.00, 3.74, 12.00, 82.74, 0.00], "cir_bm": [5.80, 1.82, 6.25, 19.10, 71.21, 0.21]},
    {"q": "3Q 2024", "sq": [0.36, 0.36, 6.90, 2.63, 1.02, 0.00], "sq_bm": [0.28, 0.05, 4.60, 1.20, 0.40, 1.89], "cir": [20.69, 0.00, 4.69, 12.54, 68.25, 0.00], "cir_bm": [6.32, 1.89, 4.51, 19.20, 83.36, 0.25]},
    {"q": "4Q 2024", "sq": [0.00, 0.00, 5.10, 1.45, 0.60, 0.19], "sq_bm": [0.14, 0.01, 4.55, 1.24, 0.41, 1.90], "cir": [14.10, 0.19, 4.16, 11.80, 83.30, 0.12], "cir_bm": [7.00, 1.90, 4.35, 19.10, 71.83, 0.24]},
    {"q": "1Q 2025", "sq": [1.59, 0.80, 4.17, 3.02, 0.00, 6.69], "sq_bm": [0.12, 0.03, 4.96, 1.26, 0.43, 1.91], "cir": [12.50, 6.69, 1.43, 12.87, 70.00, 0.00], "cir_bm": [8.23, 1.91, 3.97, 19.15, 83.7
