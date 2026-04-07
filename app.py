import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# ======================
# PAGE SETTINGS
# ======================
st.set_page_config(layout="wide")

# ======================
# AUTO REFRESH (10 sec)
# ======================
count = st_autorefresh(interval=10000, key="refresh")

# ======================
# PROFESSIONAL STYLE
# ======================
st.markdown("""
<style>

body {
    background-color:#0e1117;
}

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:700;
    color:white;
    margin-bottom:5px;
}

.sub-title{
    text-align:center;
    font-size:20px;
    color:#9ecbff;
    margin-bottom:40px;
}

.circle-container{
    display:flex;
    justify-content:space-between;
    flex-wrap:wrap;
}

.circle-box{
    text-align:center;
}

.circle{
    width:150px;
    height:150px;
    border-radius:50%;
    background: radial-gradient(circle,#1f2a38,#0e1117);
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-size:28px;
    font-weight:bold;
    box-shadow:0 0 25px rgba(0,140,255,0.6);
    margin:auto;
}

.kpi-name{
    color:#9ecbff;
    font-size:16px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ======================
# DATA (من الصورة)
# ======================
data = [
    {"Month":"1Q 2024","Patient Falls":0.24,"Injury Falls":0.26,"Pressure Injury":14.29,"CLABSI":2.47,"VAE":2.48,"CAUTI":0.98},
    {"Month":"2Q 2024","Patient Falls":0.31,"Injury Falls":0.30,"Pressure Injury":6.90,"CLABSI":2.63,"VAE":0,"CAUTI":1.02},
    {"Month":"3Q 2024","Patient Falls":0.00,"Injury Falls":0.01,"Pressure Injury":9.54,"CLABSI":1.80,"VAE":1.10,"CAUTI":1.13},
    {"Month":"1Q 2025","Patient Falls":1.59,"Injury Falls":0.80,"Pressure Injury":4.17,"CLABSI":3.02,"VAE":6.69,"CAUTI":0.00},
]

df = pd.DataFrame(data)

# اختيار شهر تلقائي
index = count % len(df)
row = df.iloc[index]

# ======================
# TITLES
# ======================
st.markdown(
    f"""
    <div class="main-title">ICU Performance Dashboard - Riyadh</div>
    <div class="sub-title">Month: {row['Month']}</div>
    """,
    unsafe_allow_html=True
)

# ======================
# KPI CIRCLES
# ======================
kpis = row.drop("Month")

html = '<div class="circle-container">'

for name, value in kpis.items():
    html += f"""
        <div class="circle-box">
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
chart_df = pd.DataFrame({
    "KPI": kpis.index,
    "Value": kpis.values
})

fig = px.bar(chart_df, x="KPI", y="Value", text="Value")

fig.update_layout(
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)
