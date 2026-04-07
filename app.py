import streamlit as st
import pandas as pd
import time

st.set_page_config(layout="wide")

# STYLE
st.markdown("""
<style>
body {background-color:#0E1117;}

.title{
text-align:center;
font-size:42px;
color:white;
font-weight:bold;
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
width:160px;
height:160px;
border-radius:50%;
background:#1f2937;
color:white;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
margin:15px;
box-shadow:0 0 25px rgba(0,150,255,0.5);
}

.kpi-name{
font-size:14px;
color:#9CA3AF;
text-align:center;
}

.kpi-value{
font-size:34px;
font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# LOAD EXCEL
df = pd.read_excel("GlobCare -KPI_Dashboard_v5.xlsx")

months = df.iloc[:,0]
metrics = df.columns[1:]

placeholder = st.empty()

# LIVE LOOP
while True:
    for i in range(len(df)):

        circles = ""

        for metric in metrics:
            value = df.loc[i, metric]

            circles += f"""
<div class="circle">
<div class="kpi-name">{metric}</div>
<div class="kpi-value">{value}</div>
</div>
"""

        placeholder.markdown(f"""
<div class="title">GlobCare Dashboard</div>
<div class="month">Month: {months[i]}</div>

<div class="container">
{circles}
</div>
""", unsafe_allow_html=True)

        time.sleep(10)
