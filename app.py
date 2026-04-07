import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(layout="wide")

# ---------- PROFESSIONAL STYLE ----------
st.markdown("""
<style>

html, body, [class*="css"] {
    background:#0b1220;
    color:white;
    font-family: 'Segoe UI', sans-serif;
}

.title{
    text-align:center;
    font-size:42px;
    font-weight:600;
    margin-bottom:5px;
}

.month{
    text-align:center;
    color:#94a3b8;
    margin-bottom:35px;
}

.grid{
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(200px,1fr));
    gap:25px;
    padding:10px 40px;
}

.card{
    background:#111827;
    border-radius:18px;
    padding:20px;
    text-align:center;
    box-shadow:0 6px 20px rgba(0,0,0,0.4);
}

.kpi-name{
    font-size:14px;
    color:#9ca3af;
    min-height:45px;
    margin-bottom:15px;
}

.circle{
    width:130px;
    height:130px;
    margin:auto;
    border-radius:50%;
    background:linear-gradient(145deg,#1f2937,#020617);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:28px;
    font-weight:bold;
    box-shadow:0 0 18px rgba(59,130,246,0.4);
}

</style>
""", unsafe_allow_html=True)

# ---------- LOAD EXCEL ----------
df = pd.read_excel("GlobCare -KPI_Dashboard_v5.xlsx")

months = df.iloc[:,0]
metrics = df.columns[1:]

header = st.empty()
chart_area = st.empty()

# ---------- LIVE DASHBOARD ----------
while True:

    for i in range(len(df)):

        cards = ""
        values = []

        for metric in metrics:
            value = df.loc[i, metric]
            values.append(value)

            cards += f"""
            <div class="card">
                <div class="kpi-name">{metric}</div>
                <div class="circle">{value}</div>
            </div>
            """

        header.markdown(f"""
        <div class="title">GlobCare Performance Dashboard</div>
        <div class="month">Month: {months[i]}</div>

        <div class="grid">
        {cards}
        </div>
        """, unsafe_allow_html=True)

        # -------- BAR CHART ----------
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
            plot_bgcolor="#0b1220",
            paper_bgcolor="#0b1220",
            font_color="white",
            xaxis_title="",
            yaxis_title=""
        )

        chart_area.plotly_chart(fig, use_container_width=True)

        time.sleep(10)
