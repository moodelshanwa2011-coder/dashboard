import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg,#0b1220,#111827,#020617);
    color:white;
}

.title{
    text-align:center;
    font-size:44px;
    font-weight:bold;
}

.month{
    text-align:center;
    font-size:22px;
    color:#cbd5e1;
    margin-bottom:30px;
}

.container{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
}

.kpi-block{
    display:flex;
    flex-direction:column;
    align-items:center;
    margin:18px;
}

.kpi-name{
    margin-bottom:10px;
    color:#94a3b8;
    font-size:15px;
}

.circle{
    width:160px;
    height:160px;
    border-radius:50%;
    background:#1f2937;
    display:flex;
    justify-content:center;
    align-items:center;
    font-size:34px;
    font-weight:bold;
    box-shadow:0 0 30px rgba(0,150,255,0.4);
}

</style>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
df = pd.read_excel("GlobCare -KPI_Dashboard_v5.xlsx")

months = df.iloc[:,0]
metrics = df.columns[1:]

top = st.empty()
chart_area = st.empty()

# ---------- LIVE LOOP ----------
while True:
    for i in range(len(df)):

        # ===== KPI CIRCLES =====
        blocks = ""

        values = []

        for metric in metrics:
            value = df.loc[i, metric]
            values.append(value)

            blocks += f"""
<div class="kpi-block">
<div class="kpi-name">{metric}</div>
<div class="circle">{value}</div>
</div>
"""

        top.markdown(f"""
<div class="title">GlobCare Performance Dashboard</div>
<div class="month">Month: {months[i]}</div>

<div class="container">
{blocks}
</div>
""", unsafe_allow_html=True)

        # ===== BAR CHART =====
        chart_df = pd.DataFrame({
            "KPI": metrics,
            "Value": values
        })

        fig = px.bar(
            chart_df,
            x="KPI",
            y="Value",
            text="Value",
            height=420
        )

        fig.update_layout(
            plot_bgcolor="#020617",
            paper_bgcolor="#020617",
            font_color="white"
        )

        chart_area.plotly_chart(fig, use_container_width=True)

        time.sleep(10)
