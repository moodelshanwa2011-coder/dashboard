import streamlit as st
import pandas as pd
import time
import plotly.express as px

st.set_page_config(layout="wide")

# ======================
# AUTO REFRESH (10 sec)
# ======================
if "counter" not in st.session_state:
    st.session_state.counter = 0

time.sleep(10)
st.session_state.counter += 1
st.rerun()

# ======================
# SAMPLE DATA (من الصورة)
# ======================
data = [
    ["Jan-2026",0.01,9.54,1.8,1.1,1.13],
    ["Feb-2026",0.02,6.67,3.02,6.69,0.54],
    ["Mar-2026",0.00,3.33,3.87,3.39,0.94],
]

df = pd.DataFrame(data,
columns=["Month","Injury","Pressure","CLABSI","VAE","CAUTI"])

row = df.iloc[st.session_state.counter % len(df)]

# ======================
# PROFESSIONAL STYLE
# ======================
st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#020617,#0f172a);
color:white;
}

.title{
text-align:center;
font-size:42px;
font-weight:bold;
margin-bottom:10px;
}

.month{
text-align:center;
font-size:20px;
color:#94a3b8;
margin-bottom:40px;
}

.kpi-grid{
display:flex;
justify-content:center;
gap:45px;
flex-wrap:wrap;
margin-bottom:50px;
}

.kpi-box{
text-align:center;
}

.kpi-name{
font-size:20px;
margin-bottom:15px;
color:#cbd5e1;
font-weight:600;
}

.circle{
width:140px;
height:140px;
border-radius:50%;
background:#1e293b;
display:flex;
align-items:center;
justify-content:center;
font-size:28px;
font-weight:bold;
box-shadow:0 0 25px rgba(0,150,255,0.6);
}

</style>
""", unsafe_allow_html=True)

# ======================
# TITLE
# ======================
st.markdown('<div class="title">GlobCare Performance Dashboard</div>', unsafe_allow_html=True)
st.markdown(f'<div class="month">Month: {row["Month"]}</div>', unsafe_allow_html=True)

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

# ======================
# BAR CHART
# ======================
chart_df = pd.DataFrame({
"KPI": kpis.index,
"Value": kpis.values
})

fig = px.bar(
chart_df,
x="KPI",
y="Value",
text="Value"
)

fig.update_layout(
plot_bgcolor="#020617",
paper_bgcolor="#020617",
font_color="white"
)

st.plotly_chart(fig, use_container_width=True)
