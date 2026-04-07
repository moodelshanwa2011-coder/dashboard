import streamlit as st
import pandas as pd
import time

# ---------- PAGE ----------
st.set_page_config(
    page_title="GlobCare Dashboard",
    layout="wide"
)

# ---------- DARK PROFESSIONAL STYLE ----------
st.markdown("""
<style>

body {
    background-color:#0E1117;
}

.title{
    text-align:center;
    font-size:42px;
    font-weight:700;
    color:white;
    margin-bottom:5px;
}

.month{
    text-align:center;
    font-size:22px;
    color:#AAAAAA;
    margin-bottom:30px;
}

.container{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
}

.circle{
    width:170px;
    height:170px;
    border-radius:50%;
    background:linear-gradient(145deg,#1f2937,#111827);
    box-shadow:
        0 0 25px rgba(0,150,255,0.4),
        inset 0 0 20px rgba(255,255,255,0.05);
    color:white;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    margin:18px;
    transition:0.4s;
}

.circle:hover{
    transform:scale(1.05);
}

.kpi-name{
    font-size:15px;
    color:#9CA3AF;
    text-align:center;
    padding:0 10px;
}

.kpi-value{
    font-size:34px;
    font-weight:bold;
    margin-top:6px;
}

</style>
""", unsafe_allow_html=True)

# ---------- LOAD EXCEL ----------
df = pd.read_excel("GlobCare -KPI_Dashboard_v5.xlsx")

months = df.iloc[:,0]      # أول عمود = الشهر
metrics = df.columns[1:]   # باقي الأعمدة = أسماء KPI الحقيقية

placeholder = st.empty()

# ---------- LIVE LOOP ----------
while True:
    for i in range(len(df)):

        circles_html = ""

        for metric in metrics:
            value = df.loc[i, metric]

            circles_html += f"""
            <div class="circle">
                <div class="kpi-name">{metric}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """

        placeholder.markdown(f"""
        <div class="title">GlobCare Performance Dashboard</div>
        <div class="month">Month: {months[i]}</div>

        <div class="container">
            {circles_html}
        </div>
        """, unsafe_allow_html=True)

        time.sleep(10)
