import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# ======================
# PAGE
# ======================
st.set_page_config(layout="wide")

# AUTO REFRESH 10 sec
count = st_autorefresh(interval=10000, key="refresh")

# ======================
# STYLE
# ======================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(180deg,#0b1320,#06090f);
}

/* TITLE */
.title {
    text-align:center;
    font-size:44px;
    font-weight:700;
    color:white;
}

.subtitle {
    text-align:center;
    font-size:20px;
    color:#8ecbff;
    margin-bottom:40px;
}

/* KPI GRID */
.kpi-grid{
    display:flex;
    justify-content:center;
    gap:60px;
    flex-wrap:wrap;
}

/* KPI NAME */
.kpi-name{
    text-align:center;
    color:#9fd3ff;
    font-size:18px;
    margin-bottom:12px;
}

/* CIRCLE */
.circle{
    width:170px;
    height:170px;
    border-radius:50%;
    background: radial-gradient(circle at 30% 30%, #1c2b3f, #09101a);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:34px;
    font-weight:bold;
    color:white;
    box-shadow:
        0 0 30px rgba(0,150,255,0.6),
        inset 0 0 20px rgba(255,255,255,0.05);
}

.kpi-box{
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ======================
# DATA (من الصورة)
# ======================
data = [
    {"Month":"1Q 2024","Falls":0.24,"Injury":0.26,"Pressure":14.29,"CLABSI":2.47,"VAE":2.48,"CAUTI":0.98},
    {"Month":"2Q 2024","Falls":0.31,"Injury":0.30,"Pressure":6.9,"CLABSI":2.63,"VAE":0.0,"CAUTI":1.02},
    {"Month":"3Q 2024","Falls":0.00,"Injury":0.01,"Pressure":9.54,"CLABSI":1.80,"VAE":1.10,"CAUTI":1.13},
    {"Month":"1Q 2025","Falls":1.59,"Injury":0.80,"Pressure":4.17,"CLABSI":3.02,"VAE":6.69,"CAUTI":0.00},
]

df = pd.DataFrame(data)

# CHANGE MONTH AUTO
row = df.iloc[count % len(df)]

# ======================
# TITLES
# ======================
st.markdown(
    f"""
    <div class="title">ICU Performance Dashboard - Riyadh</div>
    <div class="subtitle">Month: {row['Month']}</div>
    """,
    unsafe_allow_html=True
)

# ======================
# KPI CIRCLES
# ======================
kpis = row.drop("Month")

html = '<div class="kpi-grid">'

for name, value in kpis.items():
    html += f"""
    <div class="kpi-box">
        <div class="kpi-name">{name}</div>
        <div class="circle">{value}</div>
    </div>
    """

html += "</div>"

st.markdown(html, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ======================
# BAR CHART
# ======================
fig = go.Figure(
    go.Bar(
        x=list(kpis.index),
        y=list(kpis.values),
        text=list(kpis.values),
        textposition="outside"
    )
)

fig.update_layout(
    plot_bgcolor="#06090f",
    paper_bgcolor="#06090f",
    font_color="white",
    height=450
)

st.plotly_chart(fig, use_container_width=True)
