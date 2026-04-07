import streamlit as st
import pandas as pd
import time

st.set_page_config(layout="wide")

# ---------- PROFESSIONAL STYLE ----------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg,#0b1220,#111827,#020617);
    color:white;
}

/* TITLE */
.title{
    text-align:center;
    font-size:46px;
    font-weight:700;
    margin-top:10px;
}

.month{
    text-align:center;
    font-size:22px;
    color:#cbd5e1;
    margin-bottom:35px;
}

/* GRID */
.container{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
    align-items:center;
}

/* KPI BLOCK */
.kpi-block{
    display:flex;
    flex-direction:column;
    align-items:center;
    margin:20px;
}

/* KPI NAME ABOVE */
.kpi-name{
    font-size:16px;
    margin-bottom:12px;
    color:#94a3b8;
    font-weight:500;
    text-align:center;
}

/* CIRCLE */
.circle{
    width:170px;
    height:170px;
    border-radius:50%;
    background: radial-gradient(circle at 30% 30%, #1f2937, #020617);
    display:flex;
    justify-content:center;
    align-items:center;
    font-size:36px;
    font-weight:bold;
    box-shadow:
        0 0 35px rgba(0,150,255,0.35),
        inset 0 0 25px rgba(255,255,255,0.05);
    transition:0.4s;
}

.circle:hover{
    transform:scale(1.08);
}

</style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
df = pd.read_excel("GlobCare -KPI_Dashboard_v5.xlsx")

months = df.iloc[:,0]
metrics = df.columns[1:]

placeholder = st.empty()

# ---------- LIVE DISPLAY ----------
while True:
    for i in range(len(df)):

        blocks = ""

        for metric in metrics:
            value = df.loc[i, metric]

            blocks += f"""
<div class="kpi-block">
    <div class="kpi-name">{metric}</div>
    <div class="circle">{value}</div>
</div>
"""

        placeholder.markdown(f"""
<div class="title">GlobCare Performance Dashboard</div>
<div class="month">Month: {months[i]}</div>

<div class="container">
{blocks}
</div>
""", unsafe_allow_html=True)

        time.sleep(10)
