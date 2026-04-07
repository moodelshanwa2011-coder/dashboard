import streamlit as st
import pandas as pd
import time

st.set_page_config(layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.title{
    text-align:center;
    font-size:40px;
    color:white;
    font-weight:bold;
}

.month{
    text-align:center;
    font-size:20px;
    color:gray;
    margin-bottom:25px;
}

.container{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
}

.circle{
    width:150px;
    height:150px;
    border-radius:50%;
    background:#1f2937;
    color:white;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    margin:15px;
    box-shadow:0 0 20px rgba(0,150,255,0.4);
}

.kpi-name{
    font-size:14px;
    color:#9CA3AF;
    text-align:center;
}

.kpi-value{
    font-size:30px;
    font-weight:bold;
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

        html = ""

        for metric in metrics:
            value = df.loc[i, metric]

            html += f"""
<div class="circle">
<div class="kpi-name">{metric}</div>
<div class="kpi-value">{value}</div>
</div>
"""

        placeholder.markdown(
            f"""
<div class="title">GlobCare Dashboard</div>
<div class="month">Month: {months[i]}</div>

<div class="container">
{html}
</div>
""",
            unsafe_allow_html=True
        )

        time.sleep(10)
